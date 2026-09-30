from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embedding


def generate_embeddings_for_chunks(db: Session) -> int:
    """
    Generate embeddings for all document chunks
    that don't already have one.
    """

    chunks = (
        db.query(DocumentChunk)
        .filter(DocumentChunk.embedding.is_(None))
        .order_by(DocumentChunk.id)
        .all()
    )

    processed = 0

    for chunk in chunks:
        chunk.embedding = generate_embedding(
            chunk.content
        )

        processed += 1

    db.commit()

    return processed