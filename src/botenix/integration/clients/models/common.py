from pydantic import BaseModel, Field


class TimestampMixin(BaseModel):
    create_at: int = Field(..., description="Timestamp in milliseconds when the entity was created")
    update_at: int = Field(..., description="Timestamp in milliseconds when the entity was last updated")
    delete_at: int = Field(..., description="Timestamp in milliseconds when the entity was deleted")
    edit_at: int = Field(..., description="Timestamp in milliseconds when the entity was last edited")
