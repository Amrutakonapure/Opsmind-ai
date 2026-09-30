from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.user import User
from app.schemas.document import (
    DocumentResponse,
    DocumentChunkResponse
)
from app.services.document_service import (
    extract_text_from_file,
    chunk_text
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf"}


@router.post(
    "/",
    response_model=DocumentResponse
)
async def upload_document(
    file: UploadFile = File(...),
    description: str | None = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only .txt, .md and .pdf files are supported"
        )

    safe_filename = Path(file.filename).name

    file_path = UPLOAD_DIR / safe_filename

    file_content = await file.read()

    file_path.write_bytes(file_content)

    try:
        text = extract_text_from_file(
            str(file_path),
            extension
        )

        if not text.strip():
            file_path.unlink(missing_ok=True)

            raise HTTPException(
                status_code=400,
                detail="The uploaded document contains no readable text"
            )

        document = Document(
            filename=safe_filename,
            document_type=extension.replace(".", "").upper(),
            description=description
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):
            document_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk
            )

            db.add(document_chunk)

        db.commit()

        return document

    except HTTPException:
        raise

    except Exception as error:
        db.rollback()
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(error)}"
        )


@router.get(
    "/",
    response_model=list[DocumentResponse]
)
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Document)
        .order_by(Document.uploaded_at.desc())
        .all()
    )


@router.get(
    "/{document_id}/chunks",
    response_model=list[DocumentChunkResponse]
)
def get_document_chunks(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return (
        db.query(DocumentChunk)
        .filter(DocumentChunk.document_id == document_id)
        .order_by(DocumentChunk.chunk_index)
        .all()
    )