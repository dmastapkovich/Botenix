from pydantic import BaseModel, Field


class FileInfo(BaseModel):
    id: str = Field(..., description="Unique ID of the file")
    user_id: str = Field(..., description="ID of the user who created the file")
    post_id: str | None = Field(None, description="ID of the post associated with the file")
    channel_id: str = Field(..., description="ID of the channel associated with the file")
    create_at: int = Field(..., description="Timestamp of file creation")
    update_at: int = Field(..., description="Timestamp of last update")
    delete_at: int = Field(..., description="Timestamp of deletion")
    name: str = Field(..., description="Name of the file")
    extension: str = Field(..., description="File extension")
    size: int = Field(..., description="Size of the file in bytes")
    mime_type: str = Field(..., description="MIME type of the file")
    width: int | None = Field(None, description="Width of the image, if applicable")
    height: int | None = Field(None, description="Height of the image, if applicable")
    has_preview_image: bool | None = Field(None, description="Indicates if the file has a preview image")
    mini_preview: bytes | None = Field(None, description="Mini preview of the file content")
    remote_id: str | None = Field(None, description="ID for files originating from remote clusters")
    archived: bool = Field(False, description="Indicates if the file is archived")
