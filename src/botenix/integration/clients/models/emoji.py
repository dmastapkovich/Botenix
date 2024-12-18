from pydantic import BaseModel, Field


class Emoji(BaseModel):
    id: str = Field(..., description="Unique ID of the emoji")
    user_id: str | None = Field(None, description="ID of the user who created the emoji")
    name: str | None = Field(None, description="Name of the emoji")
    create_at: int = Field(..., description="Timestamp of emoji creation")
    update_at: int = Field(..., description="Timestamp of last update")
    delete_at: int = Field(..., description="Timestamp of deletion")
