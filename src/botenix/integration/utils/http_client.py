from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, TypeVar, cast

import orjson
from httpx import AsyncClient, HTTPStatusError, RequestError, Response
from pydantic import BaseModel, TypeAdapter, ValidationError

from botenix.integration.annotations import RequestJson, SerializedJson
from botenix.integration.utils.authentication import BearerAuth
from botenix.logger import integration_logger as logger


if TYPE_CHECKING:
    from botenix.integration.annotations import IncEx, Method, RequestFiles, RequestQueryParam

TRequest = TypeVar("TRequest", bound=BaseModel | Sequence[BaseModel])
TResponse = TypeVar("TResponse", bound=BaseModel | Sequence[BaseModel] | bytes | SerializedJson)


class _MethodHandler:
    def __init__(self, http_client: HttpClient, method: Method) -> None:
        self._http_client = http_client
        self._method = method

    async def __call__(  # noqa: PLR0913
        self,
        path: str,
        *,
        params: RequestQueryParam | None = None,
        json: RequestJson | None = None,
        payload: TRequest | None = None,
        files: RequestFiles | None = None,
        request_model: type[TRequest] | None = None,
        response_model: type[TResponse] | None = None,
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> TResponse:
        if payload and request_model:
            json = self._prepare_request_payload(
                payload,
                request_model,
                include,
                exclude,
                by_alias,
                exclude_unset,
                exclude_defaults,
                exclude_none,
            )

        raw_response = await self._http_client.request(
            method=self._method,
            path=path,
            params=params,
            json=json,
            files=files,
        )
        return self._prepare_response_content(raw_response, response_model)

    @staticmethod
    def _prepare_request_payload(  # noqa: PLR0913, PLR0917
        payload: TRequest,
        request_model: type[TRequest],
        include: IncEx | None,
        exclude: IncEx | None,
        by_alias: bool,
        exclude_unset: bool,
        exclude_defaults: bool,
        exclude_none: bool,
    ) -> RequestJson | None:
        serialized_payload: RequestJson = TypeAdapter(request_model).dump_python(
            payload,  # type: ignore[arg-type]
            mode="json",
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        return serialized_payload

    @staticmethod
    def _prepare_response_content(
        raw_response: SerializedJson | bytes,
        response_model: type[TResponse] | None = None,
    ) -> TResponse:
        if response_model:
            response_adapter = TypeAdapter(response_model)
            try:
                return response_adapter.validate_python(raw_response)
            except ValidationError as error:
                logger.error("Response validation failed", exc_info=error)
                raise
        return cast(TResponse, raw_response)


class HttpClient:
    def __init__(
        self,
        base_url: str,
        verify_ssl: bool = True,
        timeout: float = 10.0,
        bearer_token: str | None = None,
    ) -> None:
        self._client = AsyncClient(
            base_url=base_url,
            timeout=timeout,
            verify=verify_ssl,
            auth=BearerAuth(bearer_token) if bearer_token else None,
        )

        self.get = _MethodHandler(self, "GET")
        self.post = _MethodHandler(self, "POST")
        self.put = _MethodHandler(self, "PUT")
        self.patch = _MethodHandler(self, "PATCH")
        self.delete = _MethodHandler(self, "DELETE")

    async def request(
        self,
        method: Method,
        path: str,
        *,
        params: RequestQueryParam | None = None,
        json: RequestJson | None = None,
        files: RequestFiles | None = None,
    ) -> SerializedJson | bytes:
        logger.debug(f"Sending {method} request to {path}")
        try:
            response = await self._client.request(
                method=method,
                url=path,
                params=params,
                json=json,
                files=files,
            )
            response.raise_for_status()
            return await self._fetch_response_content(response)
        except (HTTPStatusError, RequestError) as error:
            logger.exception(f"{error.__class__.__name__} for {path}")
            raise

    @staticmethod
    async def _fetch_response_content(response: Response) -> SerializedJson | bytes:
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return cast(SerializedJson, orjson.loads(response.content))
        return await response.aread()

    async def close(self) -> None:
        await self._client.aclose()
        logger.debug("HTTP client session closed")
