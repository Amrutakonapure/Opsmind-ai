from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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