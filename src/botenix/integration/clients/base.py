from botenix.integration.utils.http_client import HttpClient


class BaseApiClient:
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client
