from datetime import datetime

from pydantic import BaseModel


class SemanticSearchResult(BaseModel):
    chunk_id: int
    document_id: int
    chunk_index: int
    content: str
    distance: float
    created_at: datetime


class SemanticSearchResponse(BaseModel):
    query: str
    results: list[SemanticSearchResult]