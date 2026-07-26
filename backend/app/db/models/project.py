import uuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.project import ProjectStatus, ProjectVisibility
from app.db.models.base import Base
from app.db.models.mixins import OrganizationOwnedModel, TimestampMixin, UUIDPrimaryKeyMixin


class Project(Base, OrganizationOwnedModel, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "projects"
    __table_args__ = (UniqueConstraint("organization_id", "slug", name="uq_project_org_slug"),)

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    environment_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("environments.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    status: Mapped[ProjectStatus] = mapped_column(
        String(20), default=ProjectStatus.ACTIVE, nullable=False, index=True
    )
    visibility: Mapped[ProjectVisibility] = mapped_column(
        String(20), default=ProjectVisibility.PRIVATE, nullable=False, index=True
    )
    
    # Audit tracking
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    updated_by_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    environment = relationship("Environment", back_populates="projects", lazy="selectin")
    settings = relationship("ProjectSettings", back_populates="project", uselist=False, lazy="selectin", cascade="all, delete-orphan")
    created_by = relationship("User", foreign_keys=[created_by_id], lazy="selectin")
    updated_by = relationship("User", foreign_keys=[updated_by_id], lazy="selectin")
