from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models.service import Service
from app.schemas.service import (ServiceCreate, ServiceUpdate, ServiceResponse)


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
def get_services(
    status: str | None = Query(
        default=None,
        description="Filter services by status"
    ),
    search: str | None = Query(
        default=None,
        description="Search services by name"
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
        description="Number of services per page"
    ),
    db: Session = Depends(get_db)
):
    query = db.query(Service)

    # Filter by status
    if status:
        query = query.filter(
            Service.status == status
        )

    # Search by service name
    if search:
        query = query.filter(
            Service.name.ilike(f"%{search}%")
        )

    # Pagination
    offset = (page - 1) * limit

    return (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )


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


@router.put("/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: int,
    service_data: ServiceUpdate,
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

    update_data = service_data.model_dump(
        exclude_unset=True
    )

    if "name" in update_data:
        existing_service = (
            db.query(Service)
            .filter(
                Service.name == update_data["name"],
                Service.id != service_id
            )
            .first()
        )

        if existing_service:
            raise HTTPException(
                status_code=400,
                detail="Service with this name already exists"
            )

    for field, value in update_data.items():
        setattr(service, field, value)

    db.commit()
    db.refresh(service)

    return service