from fastapi import (APIRouter,Depends,HTTPException)
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.repository import availability_repository
from app.models.availability import Availability
from app.schemas.availability import (AvailabilityCreate,AvailabilityUpdate,AvailabilityResponse)
from app.core.permissions import (require_provider,require_authenticated_user)

router = APIRouter(prefix="/availability",tags=["Availability"])

@router.post("",response_model=AvailabilityResponse)
def create_availability(request: AvailabilityCreate,
                        db: Session = Depends(get_db),
                        current_user=Depends(require_provider)):
    overlap = availability_repository.check_overlap(db,current_user.id,request.date,request.start_time,request.end_time)

    if overlap:
        raise HTTPException(status_code=400,
                            detail="Overlapping time slot exists.")

    availability = Availability(
        provider_id=current_user.id,
        date=request.date,
        start_time=request.start_time,
        end_time=request.end_time,
        slot_duration=request.slot_duration,
        status="Available")

    return availability_repository.create_availability(db,availability)

@router.get("",response_model=list[AvailabilityResponse])
def my_availability(db: Session = Depends(get_db),
                    current_user=Depends(require_provider)):

    return availability_repository.get_provider_slots(db,current_user.id)

@router.get("/providers/{provider_id}",response_model=list[AvailabilityResponse])
def provider_slots(provider_id: int,
                   db: Session = Depends(get_db),
                    current_user=Depends(require_authenticated_user)):

    return availability_repository.get_provider_slots(db,provider_id)

@router.put("/{availability_id}",response_model=AvailabilityResponse)
def update_availability(availability_id: int,
                        request: AvailabilityUpdate,
                        db: Session = Depends(get_db),
                        current_user=Depends(require_provider)):

    availability = availability_repository.get_availability_by_id(db,availability_id)

    if not availability:
        raise HTTPException(status_code=404,
                            detail="Availability not found.")

    if availability.provider_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="You can update only your own availability.")

    availability.date = request.date
    availability.start_time = request.start_time
    availability.end_time = request.end_time
    availability.slot_duration = request.slot_duration
    availability.status = request.status

    return availability_repository.update_availability(db,availability)

@router.delete("/{availability_id}")
def delete_availability(availability_id: int,
                        db: Session = Depends(get_db),
                        current_user=Depends(require_provider)):

    availability = availability_repository.get_availability_by_id(db,availability_id)

    if not availability:
        raise HTTPException(status_code=404,
                            detail="Availability not found.")

    if availability.provider_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="You can delete only your own availability.")

    availability_repository.delete_availability(db,availability)

    return {"message": "Availability deleted successfully."}