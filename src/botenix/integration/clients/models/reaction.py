from pydantic import BaseModel, Field


class Reaction(BaseModel):
    user_id: str = Field(..., description="ID of the user who made the reaction")
    post_id: str = Field(..., description="ID of the post to which the reaction was made")
    emoji_name: str = Field(..., description="Name of the emoji used for the reaction")
    channel_id: str = Field(..., description="ID of the channel associated with the reaction")
    create_at: int | None = Field(None, description="Timestamp of reaction creation")
    update_at: int | None = Field(None, description="Timestamp of last update")
    delete_at: int | None = Field(None, description="Timestamp of deletion")
    remote_id: str | None = Field(None, description="ID for reactions originating from remote clusters")
