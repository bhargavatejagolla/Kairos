from app.db.base import Base
from app.db.models.mixins import (
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class BaseModel(
    Base,
    UUIDPrimaryKeyMixin,
    TimestampMixin,
):
    __abstract__ = True
