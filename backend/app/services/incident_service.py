from sqlalchemy.orm import Session

from app.models.incident import Incident


def get_all_incidents(
    db: Session,
    status: str | None = None,
    severity: str | None = None,
    page: int = 1,
    limit: int = 10
):
    query = db.query(Incident)

    if status:
        query = query.filter(
            Incident.status == status
        )

    if severity:
        query = query.filter(
            Incident.severity == severity
        )

    offset = (page - 1) * limit

    return (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_incident_by_id(
    db: Session,
    incident_id: int
):
    return (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )


def create_incident(
    db: Session,
    incident: Incident
):
    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident