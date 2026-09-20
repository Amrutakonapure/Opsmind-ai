from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models.comment import IncidentComment
from app.models.incident import Incident
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse


router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.post(
    "/",
    response_model=CommentResponse,
    status_code=201
)
def create_comment(
    comment_data: CommentCreate,
    db: Session = Depends(get_db)
):
    incident = (
        db.query(Incident)
        .filter(Incident.id == comment_data.incident_id)
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    user = (
        db.query(User)
        .filter(User.id == comment_data.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    comment = IncidentComment(
        incident_id=comment_data.incident_id,
        user_id=comment_data.user_id,
        comment=comment_data.comment
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


@router.get(
    "/",
    response_model=list[CommentResponse]
)
def get_comments(
    db: Session = Depends(get_db)
):
    return db.query(IncidentComment).all()


@router.get(
    "/incident/{incident_id}",
    response_model=list[CommentResponse]
)
def get_incident_comments(
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
        db.query(IncidentComment)
        .filter(IncidentComment.incident_id == incident_id)
        .all()
    )