from datetime import datetime

from sqlalchemy import (
    Text,
    DateTime,
    ForeignKey,
    Integer
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from pgvector.sqlalchemy import VECTOR

from app.core.database import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        VECTOR(384),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    document = relationship(
        "Document",
        back_populates="chunks"
    )