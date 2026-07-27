import uuid
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from typing import TYPE_CHECKING

from app.db.models.base import BaseModel

if TYPE_CHECKING:
    from app.db.models.knowledge_chunk import KnowledgeChunk

class Embedding(BaseModel):
    __tablename__ = "embeddings"

    # We do not map chunk_id directly as a foreign key column here because KnowledgeChunk has the FK to Embedding.
    # However, for a 1-to-1 relationship, we can define the back_populates.
    
    provider: Mapped[str] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(255))
    vector: Mapped[Vector] = mapped_column(Vector(1536))
    dimension: Mapped[int] = mapped_column(Integer, default=1536)
    
    # Relationships
    chunk: Mapped["KnowledgeChunk"] = relationship("KnowledgeChunk", back_populates="embedding")
