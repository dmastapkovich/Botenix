from collections.abc import Sequence
from typing import Any

from aiommbot.types.actions import Button, Select
from aiommbot.utils.common import build_url_string_without_trailing_slash
from pydantic import BaseModel, Field, HttpUrl, field_serializer, field_validator
from pydantic_extra_types.color import Color, ColorType


class AttachmentField(BaseModel):
    title: str = Field(..., description="Title of the field")
    value: Any = Field(..., description="Value of the field; supports various types")
    short: bool = Field(default=False, description="Indicates if the field is short enough for side-by-side display")


class Attachment(BaseModel):
    text: str | None = Field(None, description="Main content text of the attachment")
    pretext: str | None = Field(None, description="Text displayed before the attachment")
    actions: Sequence[Button | Select] = Field(
        default_factory=list, description="Interactive actions within the attachment"
    )

    id: int | None = Field(None, description="ID of the attachment")
    fallback: str | None = Field(None, description="Fallback text if attachment cannot be displayed")
    color: ColorType | None = Field(None, description="Hex color code for attachment border")
    author_name: str | None = Field(None, description="Name of the author")
    author_link: HttpUrl | str | None = Field(None, description="Link to the author's page")
    author_icon: HttpUrl | str | None = Field(None, description="URL for the author's icon")
    title: str | None = Field(None, description="Title of the attachment")
    title_link: HttpUrl | str | None = Field(None, description="URL for the title link")
    fields: Sequence[AttachmentField] = Field(default_factory=list, description="Additional fields in the attachment")
    image_url: HttpUrl | str | None = Field(None, description="URL of an image displayed in the attachment")
    thumb_url: HttpUrl | str | None = Field(None, description="URL for a thumbnail image")
    footer: str | None = Field(None, description="Footer text of the attachment")
    footer_icon: HttpUrl | str | None = Field(None, description="URL of the footer icon")
    timestamp: str | int | None = Field(None, description="Timestamp associated with the attachment")

    @field_validator("author_link", "author_icon", "title_link", "image_url", "thumb_url", "footer_icon")
    @classmethod
    def validate_http_url(cls, value: str | HttpUrl) -> HttpUrl | None:
        if not value:
            return None
        if isinstance(value, str):
            return HttpUrl(value)
        return value

    @field_validator("color")
    @classmethod
    def validate_color(cls, color: ColorType) -> Color | None:
        if not color:
            return None
        return Color(color)

    @field_serializer("color", when_used="json")
    def serialize_color(self, color: ColorType) -> str | None:  # noqa: PLR6301
        if not color:
            return None
        if isinstance(color, Color):
            return color.as_hex()
        return Color(color).as_hex()

    def prepare_integration(self, webhook_url: str) -> None:
        for action in self.actions:
            action.integration.url = build_url_string_without_trailing_slash(webhook_url, action.id)
