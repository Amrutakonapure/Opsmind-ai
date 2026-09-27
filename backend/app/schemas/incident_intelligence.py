from datetime import datetime

from pydantic import BaseModel


class IncidentDetailLog(BaseModel):
    id: int
    level: str
    message: str
    source: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class IncidentDetailComment(BaseModel):
    id: int
    user_id: int
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True


class IncidentDetailsResponse(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    status: str

    service_id: int
    service_name: str

    created_by: int
    creator_name: str

    assigned_to: int | None
    assignee_name: str | None

    created_at: datetime
    resolved_at: datetime | None

    logs: list[IncidentDetailLog]
    comments: list[IncidentDetailComment]


class ServiceHealthResponse(BaseModel):
    service_id: int
    service_name: str
    service_status: str

    total_incidents: int
    open_incidents: int
    critical_incidents: int

    recent_logs: list[IncidentDetailLog]