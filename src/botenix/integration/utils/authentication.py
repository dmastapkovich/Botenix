from collections.abc import Generator

from httpx import Auth, Request, Response

from botenix.exceptions import BearerTokenMissingError


class BearerAuth(Auth):
    def __init__(self, token: str) -> None:
        if not token:
            raise BearerTokenMissingError("Bearer token is mandatory")
        self.token = token

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request
