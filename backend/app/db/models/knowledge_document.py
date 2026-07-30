import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel

if TYPE_CHECKING:
    from app.db.models.knowledge_chunk import KnowledgeChunk

class KnowledgeDocument(BaseModel):
    __tablename__ = "knowledge_documents"

    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    source: Mapped[str] = mapped_column(String(255)) # Runbooks, Architecture, Wiki, Postmortems
    version: Mapped[int] = mapped_column(default=1)
    status: Mapped[str] = mapped_column(String(50), default="active")
    
    # Relationships
    chunks: Mapped[list["KnowledgeChunk"]] = relationship("KnowledgeChunk", back_populates="document", cascade="all, delete-orphan")
