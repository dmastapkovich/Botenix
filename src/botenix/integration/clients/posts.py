from botenix.integration.clients.base import BaseApiClient
from botenix.integration.clients.models.posts import PostCreateRequest, PostResponse


class PostClient(BaseApiClient):
    async def create_post(self, post_data: PostCreateRequest) -> PostResponse:
        return await self.http_client.post[PostCreateRequest, PostResponse]("/posts", json=post_data)
