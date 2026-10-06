from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.ai_analysis import AIAnalysisResponse
from app.services.incident_analysis_service import analyze_incident


router = APIRouter(
    prefix="/ai",
    tags=["AI Analysis"]
)


@router.post(
    "/incidents/{incident_id}/analyze",
    response_model=AIAnalysisResponse
)
def analyze_incident_endpoint(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return analyze_incident(
            db=db,
            incident_id=incident_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {str(e)}"
        )