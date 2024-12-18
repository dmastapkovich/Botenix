from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class PostEmbedType(StrEnum):
    image = "image"
    message_attachment = "message_attachment"
    opengraph = "opengraph"
    link = "link"
    permalink = "permalink"
    boards = "boards"


class PostEmbed(BaseModel):
    type: PostEmbedType = Field(..., description="Type of embedded content")
    url: str | None = Field(None, description="URL of the embedded content")
    data: Any | None = Field(None, description="Additional data for the embedded content")
