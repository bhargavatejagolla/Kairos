from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.organization import OrganizationStatus
from app.db.models.base import BaseModel

if TYPE_CHECKING:
    from app.db.models.organization_member import OrganizationMember
    from app.db.models.user import User


class Organization(BaseModel):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    slug: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(String, nullable=True)

    logo_url: Mapped[str | None] = mapped_column(String, nullable=True)

    website: Mapped[str | None] = mapped_column(String, nullable=True)

    status: Mapped[OrganizationStatus] = mapped_column(
        Enum(
            OrganizationStatus,
            name="organization_status",
        ),
        default=OrganizationStatus.ACTIVE,
        nullable=False,
    )

    created_by_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    created_by: Mapped["User"] = relationship(foreign_keys=[created_by_id])

    members: Mapped[list["OrganizationMember"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
