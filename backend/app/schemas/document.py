from datetime import datetime
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    filename: str
    document_type: str
    description: str | None
    uploaded_at: datetime

    class Config:
        from_attributes = True


class DocumentChunkResponse(BaseModel):
    id: int
    document_id: int
    chunk_index: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True