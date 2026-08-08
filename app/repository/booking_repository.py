from sqlalchemy.orm import Session
from app.models.booking import Booking
from datetime import date,time
from app.utils.pagination import paginate

def create_booking(db: Session, booking: Booking):
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_booking_by_id(db: Session, booking_id: int):
    return (db.query(Booking).filter(Booking.id == booking_id,
                                    Booking.is_deleted == False).first())

def get_all_bookings(db: Session):
    return (db.query(Booking).filter(Booking.is_deleted == False).all())

def check_slot_booked(db: Session,provider_id: int,appointment_date: date,
                      start_time: time,end_time: time):
    return (db.query(Booking).filter(
            Booking.provider_id == provider_id,
            Booking.appointment_date == appointment_date,
            Booking.start_time < end_time,
            Booking.end_time > start_time,
            Booking.status != "Cancelled",
            Booking.is_deleted == False).first())

def check_duplicate_booking(db: Session,customer_id: int,service_id: int,
                            appointment_date: date,start_time: time):
    return (db.query(Booking).filter(
            Booking.customer_id == customer_id,
            Booking.service_id == service_id,
            Booking.appointment_date == appointment_date,
            Booking.start_time == start_time,
            Booking.status != "Cancelled",
            Booking.is_deleted == False).first())

def update_booking(db: Session, booking: Booking):
    db.commit()
    db.refresh(booking)
    return booking

def get_customer_bookings(db: Session,customer_id: int):
    return (db.query(Booking).filter(
            Booking.customer_id == customer_id,Booking.is_deleted == False).all())

def get_provider_upcoming_bookings(db: Session,provider_id: int):
    return (db.query(Booking).filter(
            Booking.provider_id == provider_id,
            Booking.appointment_date >= date.today(),
            Booking.status == "Confirmed",
             Booking.is_deleted == False).all())

def get_bookings(db, page=1, size=10, status=None, appointment_date=None):
    query = db.query(Booking).filter(Booking.is_deleted == False)
    if status:
        query = query.filter(Booking.status == status)
    if appointment_date:
        query = query.filter(Booking.appointment_date == appointment_date)
    query = query.order_by(Booking.appointment_date.desc())
    return paginate(query, page, size)

def delete_booking(db: Session, booking: Booking):
    booking.is_deleted = True
    db.commit()
    db.refresh(booking)
    return booking