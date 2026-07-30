from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.organization import MembershipStatus
from app.db.models.base import BaseModel

if TYPE_CHECKING:
    from app.db.models.organization import Organization
    from app.db.models.role import Role
    from app.db.models.user import User


class OrganizationMember(BaseModel):
    __tablename__ = "organization_members"
    
    __table_args__ = (
        UniqueConstraint("organization_id", "user_id", name="uq_org_user"),
    )

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role_id: Mapped[UUID] = mapped_column(
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    invited_by_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    joined_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
    
    status: Mapped[MembershipStatus] = mapped_column(
        Enum(MembershipStatus, name="membership_status"),
        default=MembershipStatus.ACTIVE,
        nullable=False,
        index=True,
    )

    organization: Mapped[Organization] = relationship(
        "Organization",
        back_populates="members",
    )

    role: Mapped[Role] = relationship(
        "Role",
        back_populates="members",
    )

    user: Mapped[User] = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="organizations",
    )

    invited_by: Mapped[User | None] = relationship(
        "User",
        foreign_keys=[invited_by_id],
    )
