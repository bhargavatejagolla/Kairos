from sqlalchemy import Column, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.enums import RuntimeType, ServiceStatus, ServiceTier, ServiceType
from app.db.models.mixins import AuditMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Service(Base, UUIDPrimaryKeyMixin, TimestampMixin, AuditMixin):
    __tablename__ = "services"

    organization_id = Column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    environment_id = Column(ForeignKey("environments.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    description = Column(String)
    
    service_type = Column(Enum(ServiceType), nullable=False, default=ServiceType.API, index=True)
    runtime = Column(Enum(RuntimeType), nullable=False, default=RuntimeType.UNKNOWN)
    tier = Column(Enum(ServiceTier), nullable=False, default=ServiceTier.TIER_3, index=True)
    status = Column(Enum(ServiceStatus), nullable=False, default=ServiceStatus.HEALTHY, index=True)
    
    repository_url = Column(String)
    documentation_url = Column(String)
    dashboard_url = Column(String)
    owner_team = Column(String(255))
    
    __table_args__ = (
        UniqueConstraint("organization_id", "project_id", "slug", name="uix_org_proj_service_slug"),
    )
    
    organization = relationship("Organization", backref="services")
    project = relationship("Project", backref="services")
    environment = relationship("Environment", backref="services")
    # relationships to incidents, metrics, etc. will be mapped as they are created
