from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.repository import dashboard_repository
from app.schemas.dashboard import (AdminDashboardResponse,ProviderDashboardResponse)
from app.core.permissions import (require_admin,require_provider)

router = APIRouter(prefix="/dashboard",
                    tags=["Dashboard"])

@router.get("/admin",response_model=AdminDashboardResponse)
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)):
    return dashboard_repository.admin_dashboard(db)

@router.get("/provider",response_model=ProviderDashboardResponse)
def provider_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(require_provider)):
    return dashboard_repository.provider_dashboard(db,current_user.id)