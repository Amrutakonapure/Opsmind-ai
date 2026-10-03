from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embedding


def semantic_search(
    db: Session,
    query: str,
    limit: int = 5,
    document_id: int | None = None
):
    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if limit < 1:
        raise ValueError("Limit must be at least 1.")

    query_embedding = generate_embedding(query)

    distance = DocumentChunk.embedding.cosine_distance(
        query_embedding
    )

    query_obj = (
        db.query(
            DocumentChunk,
            distance.label("distance")
        )
        .filter(
            DocumentChunk.embedding.is_not(None)
        )
    )

    if document_id is not None:
        query_obj = query_obj.filter(
            DocumentChunk.document_id == document_id
        )

    results = (
        query_obj
        .order_by(distance)
        .limit(limit)
        .all()
    )

    return results