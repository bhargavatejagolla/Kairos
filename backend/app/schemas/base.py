from pydantic import BaseModel, ConfigDict


class SchemaBase(BaseModel):
    """Base schema for all request and response models."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="forbid",
    )
