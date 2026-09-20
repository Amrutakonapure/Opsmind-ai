from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceResponse


router = APIRouter(
    prefix="/services",
    tags=["Services"]
)


@router.post("/", response_model=ServiceResponse, status_code=201)
def create_service(
    service_data: ServiceCreate,
    db: Session = Depends(get_db)
):
    existing_service = (
        db.query(Service)
        .filter(Service.name == service_data.name)
        .first()
    )

    if existing_service:
        raise HTTPException(
            status_code=400,
            detail="Service with this name already exists"
        )

    service = Service(
        name=service_data.name,
        description=service_data.description,
        status=service_data.status
    )

    db.add(service)
    db.commit()
    db.refresh(service)

    return service


@router.get("/", response_model=list[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.query(Service).all()


@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    service = (
        db.query(Service)
        .filter(Service.id == service_id)
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    return service