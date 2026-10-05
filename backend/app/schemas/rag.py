from pydantic import BaseModel


class RAGSource(BaseModel):
    chunk_id: int
    document_id: int
    chunk_index: int
    distance: float


class RAGResponse(BaseModel):
    question: str
    answer: str
    sources: list[RAGSource]