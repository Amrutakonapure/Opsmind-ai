from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.comment import IncidentComment
from app.models.log import Log
from app.schemas.incident_intelligence import (
    IncidentDetailsResponse
)

from app.core.dependencies import get_db, get_current_user
from app.models.incident import Incident
from app.models.service import Service
from app.models.user import User
from app.schemas.incident import (
    IncidentCreate,
    IncidentUpdate,
    IncidentResponse,
)
from app.services import incident_service

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.post(
    "/",
    response_model=IncidentResponse,
    status_code=201
)
def create_incident(
    incident_data: IncidentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = (
        db.query(Service)
        .filter(Service.id == incident_data.service_id)
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )



    incident = Incident(
        title=incident_data.title,
        description=incident_data.description,
        severity=incident_data.severity,
        status=incident_data.status,
        service_id=incident_data.service_id,
        created_by=current_user.id,
        assigned_to=incident_data.assigned_to,
    )
    return incident_service.create_incident(db, incident)



from fastapi import APIRouter, Depends, HTTPException, Query

@router.get(
    "/",
    response_model=list[IncidentResponse]
)
def get_incidents(
    status: str | None = Query(
        default=None,
        description="Filter by incident status"
    ),
    severity: str | None = Query(
        default=None,
        description="Filter by incident severity"
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of incidents per page"
    ),
    db: Session = Depends(get_db)
):
    return incident_service.get_all_incidents(
        db,
        status=status,
        severity=severity,
        page=page,
        limit=limit
    )


@router.get(
    "/{incident_id}/details",
    response_model=IncidentDetailsResponse
)
def get_incident_details(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    service = (
        db.query(Service)
        .filter(Service.id == incident.service_id)
        .first()
    )

    creator = (
        db.query(User)
        .filter(User.id == incident.created_by)
        .first()
    )

    assignee = None

    if incident.assigned_to is not None:
        assignee = (
            db.query(User)
            .filter(User.id == incident.assigned_to)
            .first()
        )

    logs = (
        db.query(Log)
        .filter(Log.incident_id == incident_id)
        .order_by(Log.created_at.desc())
        .all()
    )

    comments = (
        db.query(IncidentComment)
        .filter(
            IncidentComment.incident_id == incident_id
        )
        .order_by(IncidentComment.created_at.desc())
        .all()
    )

    return {
        "id": incident.id,
        "title": incident.title,
        "description": incident.description,
        "severity": incident.severity,
        "status": incident.status,

        "service_id": incident.service_id,
        "service_name": service.name,

        "created_by": incident.created_by,
        "creator_name": creator.name,

        "assigned_to": incident.assigned_to,
        "assignee_name": (
            assignee.name
            if assignee
            else None
        ),

        "created_at": incident.created_at,
        "resolved_at": incident.resolved_at,

        "logs": logs,
        "comments": comments
    }

class IncidentStatsResponse(BaseModel):
    total: int
    open: int
    in_progress: int
    resolved: int
    critical: int
    high: int

@router.get(
    "/stats",
    response_model=IncidentStatsResponse
)
def get_incident_stats(
    db: Session = Depends(get_db)
):
    total = db.query(Incident).count()

    open_count = (
        db.query(Incident)
        .filter(Incident.status == "OPEN")
        .count()
    )

    in_progress_count = (
        db.query(Incident)
        .filter(Incident.status == "IN_PROGRESS")
        .count()
    )

    resolved_count = (
        db.query(Incident)
        .filter(Incident.status == "RESOLVED")
        .count()
    )

    critical_count = (
        db.query(Incident)
        .filter(Incident.severity == "CRITICAL")
        .count()
    )

    high_count = (
        db.query(Incident)
        .filter(Incident.severity == "HIGH")
        .count()
    )

    return {
        "total": total,
        "open": open_count,
        "in_progress": in_progress_count,
        "resolved": resolved_count,
        "critical": critical_count,
        "high": high_count
    }

class TimelineEvent(BaseModel):
    event_type: str
    description: str
    timestamp: datetime

@router.get(
    "/{incident_id}/timeline",
    response_model=list[TimelineEvent]
)
def get_incident_timeline(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    events = []

    events.append({
        "event_type": "INCIDENT_CREATED",
        "description": (
            f"Incident created: {incident.title}"
        ),
        "timestamp": incident.created_at
    })

    logs = (
        db.query(Log)
        .filter(Log.incident_id == incident_id)
        .all()
    )

    for log in logs:
        events.append({
            "event_type": "LOG",
            "description": (
                f"[{log.level}] {log.message}"
            ),
            "timestamp": log.created_at
        })

    comments = (
        db.query(IncidentComment)
        .filter(
            IncidentComment.incident_id == incident_id
        )
        .all()
    )

    for comment in comments:
        events.append({
            "event_type": "COMMENT",
            "description": comment.comment,
            "timestamp": comment.created_at
        })

    if incident.resolved_at:
        events.append({
            "event_type": "INCIDENT_RESOLVED",
            "description": "Incident resolved",
            "timestamp": incident.resolved_at
        })

    events.sort(
        key=lambda event: event["timestamp"]
    )

    return events


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse
)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = incident_service.get_incident_by_id(
        db,
        incident_id
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident


@router.put(
    "/{incident_id}",
    response_model=IncidentResponse
)
def update_incident(
    incident_id: int,
    incident_data: IncidentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    incident = incident_service.get_incident_by_id(
        db,
        incident_id                                     
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    update_data = incident_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(incident, field, value)

    if incident.status == "RESOLVED" and incident.resolved_at is None:
        incident.resolved_at = datetime.utcnow()

    db.commit()
    db.refresh(incident)

    return incident
