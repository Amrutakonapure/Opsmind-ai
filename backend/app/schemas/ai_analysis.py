from datetime import datetime

from pydantic import BaseModel, Field


class AIAnalysisResponse(BaseModel):
    id: int
    incident_id: int
    severity: str
    probable_cause: str
    recommendations: str
    confidence: float | None
    created_at: datetime

    class Config:
        from_attributes = True