from fastapi import (APIRouter,Depends)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.repository import (booking_repository,service_repository,user_repository)
from app.utils.csv_export import export_csv
from app.core.permissions import require_admin

router = APIRouter(prefix="/export",
                    tags=["Export"])

@router.get("/services")
def export_services(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)):
    services = service_repository.get_services(db)
    rows = [
        [
            s.id,
            s.name,
            s.category,
            s.price,
            s.status]
        for s in services
    ]
    filename = export_csv(
        "services.csv",
        [
            "ID",
            "Name",
            "Category",
             "Price",
            "Status"],rows)
    return FileResponse(
        filename,
        filename="services.csv"
    )

@router.get("/bookings")
def export_bookings(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)):
    bookings = booking_repository.get_all_bookings(db)
    rows = [
        [
            b.id,
            b.customer_id,
            b.provider_id,
            b.status,
            b.total_amount]
        for b in bookings]
    filename = export_csv("bookings.csv",
        [
            "Booking ID",
            "Customer",
            "Provider",
            "Status",
            "Amount"],rows)
    return FileResponse(filename,filename="bookings.csv")

@router.get("/customers")
def export_customers(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)):
    customers = [
        u for u in user_repository.get_all_users(db)
        if u.role == "Customer"]
    rows = [
        [
            c.id,
            c.full_name,
            c.email,
            c.phone]
        for c in customers]
    filename = export_csv(
        "customers.csv",
        [
            "ID",
            "Name",
            "Email",
            "Phone"],rows)
    return FileResponse(filename,filename="customers.csv")