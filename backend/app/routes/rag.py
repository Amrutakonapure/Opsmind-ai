from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User

from app.schemas.rag import RAGResponse
from app.services.rag_service import generate_rag_answer


router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


@router.get(
    "/ask",
    response_model=RAGResponse
)
def ask_rag(
    question: str = Query(..., min_length=2),
    limit: int = Query(5, ge=1, le=10),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = generate_rag_answer(
        db=db,
        question=question,
        limit=limit
    )

    return RAGResponse(
        question=question,
        answer=result["answer"],
        sources=result["sources"]
    )