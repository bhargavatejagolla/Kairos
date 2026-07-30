from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class IncidentAttachment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "incident_attachments"

    incident_id = Column(ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    uploaded_by = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    storage_key = Column(String, nullable=False, unique=True)
    size_bytes = Column(Integer, nullable=False)

    incident = relationship("Incident", backref="attachments")
    uploader = relationship("User")
