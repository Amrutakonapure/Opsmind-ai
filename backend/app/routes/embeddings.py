from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.embedding_pipeline import (
    generate_embeddings_for_chunks
)

router = APIRouter(
    prefix="/embeddings",
    tags=["Embeddings"]
)


@router.post("/generate")
def generate_document_embeddings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    processed = generate_embeddings_for_chunks(db)

    return {
        "message": "Embedding generation completed",
        "chunks_processed": processed
    }
