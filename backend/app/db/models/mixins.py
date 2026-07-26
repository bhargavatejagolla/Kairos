import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, func
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=func.now(),
        nullable=False,
    )


class UUIDPrimaryKeyMixin:
    """Mixin for UUID primary key. Uses UUIDv7 (time-ordered) as recommended for distributed systems."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid7,
    )
