import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, func
from sqlalchemy import Uuid as UUID
from sqlalchemy.orm import Mapped, declared_attr, mapped_column
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


class OrganizationOwnedModel:
    """
    Mixin for models that belong to an organization.
    
    This provides the organization_id foreign key and a generic 
    relationship back to the organization. Phase 8+ entities
    (Projects, Incidents, etc.) should inherit from this.
    """
    
    @declared_attr
    def organization_id(cls) -> Mapped[uuid.UUID]:
        from sqlalchemy import ForeignKey
        return mapped_column(
            UUID(as_uuid=True),
            ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )

    @declared_attr
    def organization(cls) -> Mapped["Organization"]:
        from sqlalchemy.orm import relationship
        return relationship(
            "Organization",
            lazy="selectin",
        )


class AuditMixin:
    """Mixin for audit tracking (created_by, updated_by)."""

    @declared_attr
    def created_by_id(cls) -> Mapped[uuid.UUID | None]:
        from sqlalchemy import ForeignKey
        return mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    @declared_attr
    def updated_by_id(cls) -> Mapped[uuid.UUID | None]:
        from sqlalchemy import ForeignKey
        return mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

