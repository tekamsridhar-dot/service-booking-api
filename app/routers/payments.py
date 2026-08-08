from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.repository import payment_repository, booking_repository
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.core.permissions import (require_customer,require_admin,require_authenticated_user)

router=APIRouter(prefix="/payments",
                 tags=["Payments"])

@router.post("",response_model=PaymentResponse)
def create_payment(request:PaymentCreate,
                   db:Session=Depends(get_db),
                   current_user=Depends(require_customer)):
    booking=booking_repository.get_booking_by_id(db,request.booking_id)
    if not booking:
        raise HTTPException(status_code=404,
                            detail="Booking not found")
    if not booking:
        raise HTTPException(status_code=404,
                            detail="Booking not found.")
    if booking.customer_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="Access denied.")
    existing = payment_repository.get_payment_by_booking(db,request.booking_id)
    if existing:
        raise HTTPException(status_code=400,
                            detail="Payment already exists.")
    payment = Payment(
        booking_id=request.booking_id,
        amount=booking.total_amount,
        payment_method=request.payment_method,
        payment_status="Paid")
    return payment_repository.create_payment(db,payment)

@router.get("/{payment_id}",response_model=PaymentResponse)
def get_payment(payment_id: int,db: Session = Depends(get_db),
                current_user=Depends(require_authenticated_user)):
    payment = payment_repository.get_payment_by_id(db,payment_id)
    if not payment:
        raise HTTPException(status_code=404,
                            detail="Payment not found.")
    booking = booking_repository.get_booking_by_id(db,payment.booking_id)
    if (current_user.role != "Admin"
        and booking.customer_id != current_user.id):
        raise HTTPException(status_code=403,
                            detail="Access denied.")
    return payment

@router.post("/{payment_id}/refund",response_model=PaymentResponse)
def refund_payment( payment_id: int,db: Session = Depends(get_db),
                    current_user=Depends(require_admin)):
    payment = payment_repository.get_payment_by_id(db,payment_id)
    if not payment:
        raise HTTPException(status_code=404,
                            detail="Payment not found.")
    if payment.payment_status != "Paid":
        raise HTTPException(status_code=400,
                            detail="Only paid payments can be refunded.")
    payment.payment_status = "Refunded"
    return payment_repository.update_payment(db,payment)