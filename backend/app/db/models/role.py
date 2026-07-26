from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel
from app.db.models.role_permission import role_permissions

if TYPE_CHECKING:
    from app.db.models.permission import Permission
    from app.db.models.organization_member import OrganizationMember


class Role(BaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
    )

    permissions: Mapped[list[Permission]] = relationship(
        secondary=role_permissions,
        back_populates="roles",
        lazy="selectin",
    )
    
    members: Mapped[list["OrganizationMember"]] = relationship(
        "OrganizationMember",
        back_populates="role",
    )
