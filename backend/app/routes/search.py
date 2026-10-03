from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.core.dependencies import get_current_user
from app.services.semantic_search import semantic_search
from app.schemas.semantic_search import (
    SemanticSearchResponse,
    SemanticSearchResult
)


router = APIRouter(
    prefix="/search",
    tags=["Semantic Search"]
)


@router.get(
    "/semantic",
    response_model=SemanticSearchResponse
)
def semantic_search_endpoint(
    query: str = Query(..., min_length=2),
    limit: int = Query(5, ge=1, le=20),
    document_id: int | None = Query(None, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = semantic_search(
        db=db,
        query=query,
        limit=limit,
        document_id=document_id
    )

    formatted_results = []

    for chunk, distance in results:
        formatted_results.append(
            SemanticSearchResult(
                chunk_id=chunk.id,
                document_id=chunk.document_id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                distance=float(distance),
                created_at=chunk.created_at
            )
        )

    return SemanticSearchResponse(
        query=query,
        results=formatted_results
    )