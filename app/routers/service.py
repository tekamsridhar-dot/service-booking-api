from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from app.dependencies import get_db,get_current_user
from app.repository import service_repository
from app.models.service import Service
from app.core.permissions import require_authenticated_user, require_authenticated_user, require_customer, require_provider,require_provider,require_admin_or_provider
from app.schemas.booking import BookingCreate
from app.schemas.service import ServiceCreate,ServiceUpdate,ServiceResponse
from typing import Optional

router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/")
def create_service(request: ServiceCreate,
                   db: Session = Depends(get_db),
                   current_user=Depends(require_provider)):
    service = Service(provider_id=current_user.id,
                      name=request.name,
                      description=request.description,
                      category=request.category,
                      duration=request.duration,
                      price=request.price,
                      status=request.status)

    return service_repository.create_service(db, service)

@router.get("",response_model=list[ServiceResponse])
def get_services(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by:str |None=None,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)):

    return service_repository.get_services(
        db=db,
        page=page,
        size=size,
        search=search,
        category=category,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by)

@router.get("/{service_id}",response_model=ServiceResponse)
def get_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)):
    service = service_repository.get_service_by_id(db,service_id)

    if not service:raise HTTPException(status_code=404,
                                       detail="Service not found.")
    return service

@router.put("/{service_id}",response_model=ServiceResponse)
def update_service(
    service_id: int,
    request: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_provider)):
    service = service_repository.get_service_by_id(db,service_id)

    if not service:raise HTTPException(status_code=404,
                                       detail="Service not found.")
    if service.provider_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="You can update only your own services.")
    update_data = request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(service, key, value)

    return service_repository.update_service(db,service)

@router.delete("/{service_id}")
def delete_service(service_id: int,
                    db: Session = Depends(get_db),
                    current_user=Depends(require_admin_or_provider)):

    service = service_repository.get_service_by_id(db,service_id)
    if not service:
        raise HTTPException(status_code=404,
                            detail="Service not found.")
    if (current_user.role.lower() == "service provider"
        and service.provider_id != current_user.id):
        raise HTTPException(status_code=403,
                            detail="You can delete only your own services.")
    service_repository.delete_service(db,service)
    return {"message": "Service deleted successfully."}

@router.put("/{booking_id}/confirm")
def confirm_booking(booking_id: int,
                    db: Session = Depends(get_db),
                    current_user=Depends(require_provider)):
    return {"message": "Booking confirmed successfully"}

@router.put("/{booking_id}/complete")
def complete_booking(booking_id: int,
                     db: Session = Depends(get_db),
                     current_user=Depends(require_provider)):
    return {"message": "Booking completed successfully"}

@router.put("/{booking_id}/cancel")
def cancel_booking(booking_id: int,
                    db: Session = Depends(get_db),
                    current_user=Depends(require_customer)):
    return {"message": "Booking canceled successfully"}

