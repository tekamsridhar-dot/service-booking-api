import os
from fastapi import (APIRouter,UploadFile,File,Depends,HTTPException)
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.core.permissions import require_provider
from app.services.file_service import save_file
from app.repository import service_repository

router = APIRouter(prefix="/upload",
                    tags=["File Upload"])

@router.post("/profile-image")
def upload_profile(file: UploadFile = File(...),
                    db: Session = Depends(get_db),
                    current_user=Depends(require_provider)):
    filename = save_file(file,"uploads/profiles")
    current_user.profile_image = (f"/uploads/profiles/{filename}")
    db.commit()
    return {"message": "Profile image uploaded.",
            "image_url": current_user.profile_image}

@router.post("/service-image/{service_id}")
def upload_service_image(service_id: int,
                        file: UploadFile = File(...),
                        db: Session = Depends(get_db),
                        current_user=Depends(require_provider)):
    service = service_repository.get_service_by_id(db,service_id)
    if not service:
        raise HTTPException(status_code=404,
                            detail="Service not found.")
    if service.provider_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="Access denied.")
    filename = save_file(file,"uploads/services")
    service.image = (f"/uploads/services/{filename}")
    db.commit()
    db.refresh(service)
    return {"message": "Service image uploaded.",
            "image_url": service.image}