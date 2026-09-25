from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.log import Log
from app.models.incident import Incident
from app.models.service import Service
from app.schemas.log import LogCreate, LogResponse
from app.models.user import User


router = APIRouter(
    prefix="/logs",
    tags=["Logs"]
)


@router.post(
    "/",
    response_model=LogResponse,
    status_code=201
)
def create_log(
    log_data: LogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = (
        db.query(Service)
        .filter(Service.id == log_data.service_id)
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    if log_data.incident_id is not None:
        incident = (
            db.query(Incident)
            .filter(Incident.id == log_data.incident_id)
            .first()
        )

        if not incident:
            raise HTTPException(
                status_code=404,
                detail="Incident not found"
            )

    log = Log(
        incident_id=log_data.incident_id,
        service_id=log_data.service_id,
        level=log_data.level,
        message=log_data.message,
        source=log_data.source
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


@router.get(
    "/",
    response_model=list[LogResponse]
)
def get_logs(
    db: Session = Depends(get_db)
):
    return db.query(Log).all()


@router.get(
    "/incident/{incident_id}",
    response_model=list[LogResponse]
)
def get_incident_logs(
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

    return (
        db.query(Log)
        .filter(Log.incident_id == incident_id)
        .all()
    )