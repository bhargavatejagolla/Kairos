from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.mixins import OrganizationOwnedModel, TimestampMixin, UUIDPrimaryKeyMixin


class Environment(Base, OrganizationOwnedModel, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "environments"
    __table_args__ = (UniqueConstraint("organization_id", "slug", name="uq_env_org_slug"),)

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    slug: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    color: Mapped[str | None] = mapped_column(String(20), nullable=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    projects = relationship("Project", back_populates="environment", cascade="all, delete-orphan")
