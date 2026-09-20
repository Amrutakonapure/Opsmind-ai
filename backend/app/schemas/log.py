from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LogCreate(BaseModel):
    incident_id: int | None = None
    service_id: int
    level: str
    message: str
    source: str | None = None


class LogResponse(BaseModel):
    id: int
    incident_id: int | None
    service_id: int
    level: str
    message: str
    source: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)