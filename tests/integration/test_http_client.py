from collections.abc import AsyncGenerator, Sequence
from contextlib import nullcontext as does_not_raise
from typing import Any

import orjson
import pytest
from httpx import RequestError
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from pytest_httpx import HTTPXMock

from botenix.integration.utils.http_client import HttpClient


class TestRequestModel(BaseModel):
    name: str
    age: int


class TestResponseModel(BaseModel):
    id: int
    name: str
    age: int


class UnknownModel(BaseModel):
    unknown: str


class ExtendedRequestModel(BaseModel):
    name: str = Field(..., alias="full_name")
    age: int
    email: str | None = None
    active: bool = True
    address: str | None = Field(default=None, alias="location")
    phone: str | None = None
    newsletter: bool = Field(default=False, alias="subscribe")

    model_config = ConfigDict(populate_by_name=True)


@pytest.fixture
async def http_client() -> AsyncGenerator[HttpClient]:
    client = HttpClient(base_url="http://testserver.com", bearer_token="test-token")
    yield client
    await client.close()


@pytest.mark.parametrize("method", ["get", "post", "put", "patch", "delete"])
async def test_http_methods_only_response_model(http_client: HttpClient, httpx_mock: HTTPXMock, method: str) -> None:
    response_data = {"id": 1, "name": "John", "age": 30}
    httpx_mock.add_response(url="http://testserver.com/test-path", json=response_data)

    method_handler = getattr(http_client, method)
    response = await method_handler("/test-path", response_model=TestResponseModel)
    assert isinstance(response, TestResponseModel)
    assert response.id == 1
    assert response.name == "John"
    assert response.age == 30


@pytest.mark.parametrize("method", ["get", "post", "put", "patch", "delete"])
async def test_http_methods_only_request_model(http_client: HttpClient, httpx_mock: HTTPXMock, method: str) -> None:
    payload = TestRequestModel(name="John", age=30)

    httpx_mock.add_response(url="http://testserver.com/test-path", json=None)

    with does_not_raise():
        method_handler = getattr(http_client, method)
        await method_handler("/test-path", request_model=TestRequestModel, payload=payload)


@pytest.mark.parametrize("method", ["get", "post", "put", "patch", "delete"])
async def test_http_methods_no_models(http_client: HttpClient, httpx_mock: HTTPXMock, method: str) -> None:
    response_data = "Success"
    httpx_mock.add_response(url="http://testserver.com/test-path", content=response_data.encode())

    method_handler = getattr(http_client, method)
    response = await method_handler("/test-path")
    assert response == response_data.encode()


async def test_sequence_response_model(http_client: HttpClient, httpx_mock: HTTPXMock) -> None:
    response_data = [
        {"id": 1, "name": "John", "age": 30},
        {"id": 2, "name": "Doe", "age": 25},
    ]

    httpx_mock.add_response(url="http://testserver.com/test-path", json=response_data)

    response = await http_client.get("/test-path", response_model=list[TestResponseModel])
    assert isinstance(response, list)
    assert len(response) == 2
    assert response[0].id == 1
    assert response[1].id == 2


async def test_sequence_request_model(http_client: HttpClient, httpx_mock: HTTPXMock) -> None:
    response_data = "Success"
    httpx_mock.add_response(url="http://testserver.com/test-path", content=response_data.encode())

    payload = [
        TestRequestModel(name="John", age=30),
        TestRequestModel(name="Doe", age=25),
    ]
    response: bytes = await http_client.post("/test-path", request_model=list[TestRequestModel], payload=payload)
    assert response == response_data.encode()


async def test_sequence_request_and_response_models(http_client: HttpClient, httpx_mock: HTTPXMock) -> None:
    response_data = [
        {"id": 1, "name": "John", "age": 30},
        {"id": 2, "name": "Doe", "age": 25},
    ]
    httpx_mock.add_response(url="http://testserver.com/test-path", json=response_data)

    payload = [
        TestRequestModel(name="John", age=30),
        TestRequestModel(name="Doe", age=25),
    ]
    response = await http_client.post(
        "/test-path",
        request_model=Sequence[TestRequestModel],
        response_model=Sequence[TestResponseModel],
        payload=payload,
    )
    assert isinstance(response, list)
    assert len(response) == 2
    assert response[0].id == 1
    assert response[1].id == 2


async def test_prepare_response_content_error(http_client: HttpClient, httpx_mock: HTTPXMock) -> None:
    response_data = {"invalid": "data"}
    httpx_mock.add_response(url="http://testserver.com/test-path", json=response_data)

    with pytest.raises(ValidationError):
        await http_client.get("/test-path", response_model=TestResponseModel)


async def test_http_client_request_errors(http_client: HttpClient, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_exception(RequestError("test error"))

    with pytest.raises(RequestError):
        await http_client.get("/test-path")


@pytest.mark.parametrize(
    ("include", "exclude", "by_alias", "exclude_unset", "exclude_defaults", "exclude_none", "expected_payload"),
    [
        (
            None,
            None,
            False,
            False,
            False,
            False,
            {
                "name": "John",
                "age": 30,
                "email": "john@example.com",
                "active": True,
                "address": "123 Main St",
                "phone": None,
                "newsletter": False,
            },
        ),
        (
            {"name", "email"},
            None,
            False,
            False,
            False,
            False,
            {"name": "John", "email": "john@example.com"},
        ),
        (
            None,
            {"age", "newsletter"},
            True,
            False,
            False,
            False,
            {
                "full_name": "John",
                "email": "john@example.com",
                "active": True,
                "location": "123 Main St",
                "phone": None,
            },
        ),
        (
            None,
            None,
            True,
            True,
            False,
            False,
            {
                "full_name": "John",
                "age": 30,
                "email": "john@example.com",
                "active": True,
                "location": "123 Main St",
                "subscribe": False,
            },
        ),
        (
            None,
            None,
            True,
            False,
            True,
            False,
            {
                "full_name": "John",
                "age": 30,
                "email": "john@example.com",
                "location": "123 Main St",
            },
        ),
        (
            None,
            None,
            True,
            False,
            False,
            True,
            {
                "full_name": "John",
                "active": True,
                "age": 30,
                "location": "123 Main St",
                "email": "john@example.com",
                "subscribe": False,
            },
        ),
    ],
)
async def test_request_with_serialization_parameters(  # noqa: PLR0913, PLR0917
    http_client: HttpClient,
    httpx_mock: HTTPXMock,
    include: dict[str, Any] | None,
    exclude: dict[str, Any] | None,
    by_alias: bool,
    exclude_unset: bool,
    exclude_defaults: bool,
    exclude_none: bool,
    expected_payload: dict[str, Any],
) -> None:
    payload = ExtendedRequestModel(
        name="John",
        age=30,
        email="john@example.com",
        active=True,
        address="123 Main St",
        newsletter=False,
    )

    httpx_mock.add_response(url="http://testserver.com/test-path", json={"success": True})

    await http_client.post(
        "/test-path",
        request_model=ExtendedRequestModel,
        payload=payload,
        include=include,
        exclude=exclude,
        by_alias=by_alias,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=exclude_none,
    )

    request = httpx_mock.get_request()
    assert request
    assert request.method == "POST"
    assert request.url == "http://testserver.com/test-path"
    assert orjson.loads(request.content) == expected_payload
