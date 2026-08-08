from fastapi import APIRouter, Depends, HTTPException,BackgroundTasks
from datetime import date
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.repository import (booking_repository,service_repository,availability_repository)
from app.models.booking import Booking
from app.schemas.booking import (BookingCreate,BookingResponse)
from app.core.permissions import (require_customer,require_authenticated_user,require_provider)
from app.services.notification_service import send_notification
from app.services.email_service import send_email


router=APIRouter(prefix="/bookings",
                 tags=["Booking"])

@router.post("",response_model=BookingResponse)
def book_appointment(
    request: BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_customer)):
    service = service_repository.get_service_by_id(db,request.service_id)
    if not service:
        raise HTTPException(status_code=404,
                            detail="Service not found.")
    if service.status != "Active":
        raise HTTPException(status_code=400,
                            detail="Service is inactive.")
    slots = availability_repository.get_provider_slots(db,request.provider_id)
    valid_slot = False
    for slot in slots:
        if (slot.date == request.appointment_date
            and slot.start_time <= request.start_time
            and slot.end_time >= request.end_time
            and slot.status == "Available"):
            valid_slot = True
            break
    if not valid_slot:
        raise HTTPException(status_code=400,
                            detail="Selected time slot is unavailable.")
    existing = booking_repository.check_slot_booked(db,
                                                    request.provider_id,
                                                    request.appointment_date,
                                                    request.start_time,
                                                    request.end_time)
    if existing:
        raise HTTPException(status_code=400,
                            detail="Time slot already booked.")
    duplicate = booking_repository.check_duplicate_booking(db,
                                                           current_user.id,
                                                           request.service_id,
                                                           request.appointment_date,
                                                           request.start_time)
    if duplicate:
        raise HTTPException(status_code=400,
                            detail="Duplicate booking.")
    booking = Booking(
        customer_id=current_user.id,
        provider_id=request.provider_id,
        service_id=request.service_id,
        appointment_date=request.appointment_date,
        start_time=request.start_time,
        end_time=request.end_time,
        total_amount=service.price,
        status="Pending")
    booking_repository.create_booking(db,booking)
    background_tasks: BackgroundTasks
    background_tasks.add_task(send_email,current_user.email,"Booking Created","<h2>Your booking has been created.</h2>")
    background_tasks.add_task(send_email,current_user.email,"Appointment Reminder","<h2>Your appointment is tomorrow.</h2>")
    send_notification(  db,booking.provider_id,"New Appointment",
                    f"You have a new appointment booking from {current_user.full_name}.")
    send_notification(  db,current_user.id,"Booking Created",
                        "Your appointment request has been submitted.")
    return booking

@router.get("",response_model=list[BookingResponse])
def get_bookings(db: Session = Depends(get_db),
                current_user=Depends(require_authenticated_user)):

    bookings = booking_repository.get_all_bookings(db)
    if current_user.role == "Admin":
        return bookings
    if current_user.role == "Customer":
        return [b for b in bookings
            if b.customer_id == current_user.id]

    return [b for b in bookings
            if b.provider_id == current_user.id]

@router.get("/my-history",response_model=list[BookingResponse])
def booking_history(db: Session = Depends(get_db),
                    current_user=Depends(require_customer)):
    return booking_repository.get_customer_bookings(db,current_user.id)

@router.get("/upcoming",response_model=list[BookingResponse])
def upcoming_bookings(db: Session = Depends(get_db),
                      current_user=Depends(require_provider)):
    return booking_repository.get_provider_upcoming_bookings(db,current_user.id)

@router.get("/{booking_id}",response_model=BookingResponse)
def get_booking(booking_id: int,
                db: Session = Depends(get_db),
                current_user=Depends(require_authenticated_user)):
    booking = booking_repository.get_booking_by_id(db,booking_id)
    if not booking:
        raise HTTPException(status_code=404,
                            detail="Booking not found.")
    if (
        current_user.role != "Admin"
        and booking.customer_id != current_user.id
        and booking.provider_id != current_user.id):
        raise HTTPException(status_code=403,
                            detail="Access denied.")
    return booking

@router.put("/{booking_id}/confirm",response_model=BookingResponse)
def confirm_booking(booking_id: int,
                    db: Session = Depends(get_db),
                    current_user=Depends(require_provider)):
    booking = booking_repository.get_booking_by_id(db,booking_id)
    if not booking:
        raise HTTPException(status_code=404,
                            detail="Booking not found.")
    if booking.provider_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="Access denied.")
    if booking.status != "Pending":
        raise HTTPException(status_code=400,
                            detail="Only pending bookings can be confirmed.")
    booking.status = "Confirmed"
    booking = booking_repository.update_booking(db, booking)
    background_tasks: BackgroundTasks
    background_tasks.add_task(send_email,current_user.email,"Booking Confirmed","<h2>Your booking is confirmed.</h2>")
    send_notification(db,booking.customer_id,"Appointment Confirmed",
                        "Your appointment has been confirmed.")
    return booking

@router.put("/{booking_id}/reject",response_model=BookingResponse)
def reject_booking( booking_id: int,
                    db: Session = Depends(get_db),
                    current_user=Depends(require_provider)):
    booking = booking_repository.get_booking_by_id(db,booking_id)
    if not booking:
        raise HTTPException(status_code=404,
                            detail="Booking not found.")
    if booking.provider_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="Access denied.")
    if booking.status != "Pending":
        raise HTTPException(status_code=400,
                            detail="Only pending bookings can be rejected.")
    booking.status = "Cancelled"
    return booking_repository.update_booking(db,booking)

@router.put("/{booking_id}/cancel",response_model=BookingResponse)
def cancel_booking( booking_id: int,
                    db: Session = Depends(get_db),
                    current_user=Depends(require_customer)):
    booking = booking_repository.get_booking_by_id(db,booking_id)
    if not booking:
        raise HTTPException(status_code=404,
                            detail="Booking not found.")
    if booking.customer_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="Access denied.")
    if booking.status not in ["Pending","Confirmed"]:
        raise HTTPException(status_code=400,
                            detail="Booking cannot be cancelled.")
    booking.status = "Cancelled"
    booking = booking_repository.update_booking(db, booking)
    background_tasks: BackgroundTasks
    background_tasks.add_task(send_email,current_user.email,"Booking Cancelled","<h2>Your booking was cancelled.</h2>")
    send_notification(db,booking.provider_id,"Appointment Cancelled",
                        "Customer cancelled the appointment.")
    return booking

@router.put("/{booking_id}/reschedule",response_model=BookingResponse)
def reschedule_booking( booking_id: int,
                        request: BookingCreate,
                        db: Session = Depends(get_db),
                        current_user=Depends(require_customer)):
    booking = booking_repository.get_booking_by_id(db,booking_id)
    if not booking:
        raise HTTPException(status_code=404,
                            detail="Booking not found.")
    if booking.customer_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="Access denied.")
    booking.appointment_date = request.appointment_date
    booking.start_time = request.start_time
    booking.end_time = request.end_time
    booking.status = "Pending"
    return booking_repository.update_booking(db,booking)

@router.put("/{booking_id}/complete",response_model=BookingResponse)
def complete_booking(   booking_id: int,
                        db: Session = Depends(get_db),
                        current_user=Depends(require_provider)):
    booking = booking_repository.get_booking_by_id(db,booking_id)
    if not booking:
        raise HTTPException(status_code=404,
                            detail="Booking not found.")
    if booking.provider_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="Access denied.")
    if booking.status != "Confirmed":
        raise HTTPException(status_code=400,
                            detail="Only confirmed bookings can be completed.")
    booking.status = "Completed"
    booking_repository.update_booking(db,booking)
    send_notification(db,booking.customer_id,"Appointment Completed",
                    "Please rate your experience.")
    return booking

@router.get("",response_model=list[BookingResponse])
def bookings(
    page: int = 1,
    size: int = 10,
    status: str = None,
    appointment_date: date = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)):
    return booking_repository.get_bookings(db,page,size,status,appointment_date)