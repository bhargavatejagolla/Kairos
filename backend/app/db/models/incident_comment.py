
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class IncidentComment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "incident_comments"

    incident_id = Column(ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    body = Column(String, nullable=False)
    edited_at = Column(DateTime(timezone=True), nullable=True)

    incident = relationship("Incident", backref="comments")
    author = relationship("User")
