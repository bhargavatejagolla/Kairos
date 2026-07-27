import uuid
from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.db.models.base import BaseModel

if TYPE_CHECKING:
    from app.db.models.knowledge_document import KnowledgeDocument
    from app.db.models.embedding import Embedding

class KnowledgeChunk(BaseModel):
    __tablename__ = "knowledge_chunks"

    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("knowledge_documents.id", ondelete="CASCADE"), index=True)
    content: Mapped[str] = mapped_column(Text)
    sequence: Mapped[int] = mapped_column(Integer)
    embedding_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("embeddings.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Relationships
    document: Mapped["KnowledgeDocument"] = relationship("KnowledgeDocument", back_populates="chunks")
    embedding: Mapped["Embedding"] = relationship("Embedding", back_populates="chunk", uselist=False)
