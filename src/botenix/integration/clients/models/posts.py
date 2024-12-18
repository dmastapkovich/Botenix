from typing import Any

from pydantic import BaseModel, Field

from botenix.integration.clients.models.common import TimestampMixin
from botenix.integration.clients.models.embed import PostEmbed
from botenix.integration.clients.models.emoji import Emoji
from botenix.integration.clients.models.file_info import FileInfo
from botenix.integration.clients.models.reaction import Reaction


class Priority(BaseModel):
    priority: str | None = Field(None, description="The priority label for the post, e.g., 'important' or 'urgent'")
    requested_ack: bool | None = Field(None, description="Whether acknowledgements were requested for the post")
    persistent_notifications: bool | None = Field(None, description="If notifications are persistent")


class PostImage(BaseModel):
    width: int = Field(..., description="Width of the image in pixels")
    height: int = Field(..., description="Height of the image in pixels")
    format: str = Field(..., description="Format of the image, e.g., 'png', 'jpeg'")
    frame_count: int = Field(0, description="Number of frames in the image if animated")


class PostAcknowledgement(BaseModel):
    user_id: str = Field(..., description="ID of the user who acknowledged the post")
    post_id: str = Field(..., description="ID of the post that was acknowledged")
    acknowledged_at: int = Field(..., description="Timestamp in milliseconds when the post was acknowledged")


class PostMetadata(BaseModel):
    embeds: list[PostEmbed] = Field(default_factory=list, description="List of embeds attached to the post")
    emojis: list[Emoji] = Field(default_factory=list, description="List of emojis used in or reacting to the post")
    files: list[FileInfo] = Field(default_factory=list, description="List of files attached to the post")
    images: dict[str, PostImage] = Field(default_factory=dict, description="External image dimensions")
    reactions: list[Reaction] = Field(default_factory=list, description="Reactions made to the post")
    priority: Priority | None = Field(None, description="Priority and notification metadata for the post")
    acknowledgements: list[PostAcknowledgement] = Field(
        default_factory=list, description="List of user acknowledgements for the post"
    )


class BasePost(BaseModel):
    channel_id: str = Field(..., description="The channel ID where the post will be created")
    message: str = Field(..., description="The content of the post, supporting Markdown formatting")
    root_id: str | None = Field(None, description="The root post ID if this post is a reply in a thread")
    file_ids: list[str] | None = Field(None, description="List of file IDs attached to the post")
    props: dict[str, Any] | None = Field(None, description="Additional JSON properties for the post")
    metadata: PostMetadata | None = Field(None, description="Additional metadata for the post")


class PostCreateRequest(BasePost):
    pass


class PostResponse(BasePost, TimestampMixin):
    id: str = Field(..., description="Unique identifier for the post")
    user_id: str = Field(..., description="ID of the user who created the post")
    original_id: str | None = Field(None, description="The ID of the original post if this is an edit")
    type: str = Field("", description="Type of the post, defining special system messages or custom types")
    pending_post_id: str | None = Field(None, description="Temporary ID for pending posts")
    hashtags: str | None = Field(None, description="Any hashtags associated with the post")
