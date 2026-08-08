from sqlalchemy.orm import Session
from app.models.payment import Payment


def create_payment(db: Session, payment:Payment):
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payment_by_id(db: Session, booking_id: int):
    return (db.query(Payment)
            .filter(Payment.id == booking_id)
            .first())

def get_payment_by_booking(db: Session,booking_id:int):
    return db.query(Payment).filter(Payment.booking_id==booking_id).first()


def update_payment(db: Session, payment: Payment):
    db.commit()
    db.refresh(payment)
    return payment