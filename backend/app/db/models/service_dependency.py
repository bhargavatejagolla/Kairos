from uuid import UUID
from sqlalchemy import Column, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.mixins import UUIDPrimaryKeyMixin, TimestampMixin
from app.db.models.enums import DependencyType

class ServiceDependency(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "service_dependencies"

    upstream_service_id = Column(ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True)
    downstream_service_id = Column(ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True)
    
    dependency_type = Column(Enum(DependencyType), nullable=False, default=DependencyType.SYNCHRONOUS)

    __table_args__ = (
        UniqueConstraint("upstream_service_id", "downstream_service_id", name="uix_service_dependency"),
    )
    
    upstream_service = relationship("Service", foreign_keys=[upstream_service_id], backref="downstream_dependencies")
    downstream_service = relationship("Service", foreign_keys=[downstream_service_id], backref="upstream_dependencies")
