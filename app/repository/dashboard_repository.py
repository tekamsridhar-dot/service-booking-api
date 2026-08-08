from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.service import Service
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.review import Review

def admin_dashboard(db: Session):
    total_users = (db.query(User).filter(User.role == "Customer").count())
    total_providers = (db.query(User).filter(User.role == "ServiceProvider").count())
    total_services = db.query(Service).count()
    total_bookings = db.query(Booking).count()
    completed_bookings = (db.query(Booking).filter(Booking.status == "Completed").count())
    cancelled_bookings = (db.query(Booking).filter(Booking.status == "Cancelled").count())
    revenue = (db.query(func.sum(Payment.amount)).filter(Payment.payment_status == "Paid").scalar())
    return {
        "total_users": total_users,
        "total_providers": total_providers,
        "total_services": total_services,
        "total_bookings": total_bookings,
        "completed_bookings": completed_bookings,
        "cancelled_bookings": cancelled_bookings,
        "total_revenue": revenue or 0}

def provider_dashboard(db: Session,provider_id: int):
    today = date.today()
    today_appointments = (db.query(Booking).filter(
            Booking.provider_id == provider_id,
            Booking.appointment_date == today).count())
    upcoming = (db.query(Booking).filter(
            Booking.provider_id == provider_id,
            Booking.appointment_date > today,
            Booking.status == "Confirmed").count())
    completed = (db.query(Booking).filter(
            Booking.provider_id == provider_id,
            Booking.status == "Completed").count())
    earnings = (db.query(func.sum(Payment.amount)).join(Booking).filter(
            Booking.provider_id == provider_id,
            Payment.payment_status == "Paid").scalar())
    average_rating = (db.query(func.avg(Review.rating)).join(Booking).filter(
            Booking.provider_id == provider_id).scalar())
    return {
        "today_appointments": today_appointments,
        "upcoming_appointments": upcoming,
        "completed_appointments": completed,
        "total_earnings": earnings or 0,
        "average_rating": round(average_rating, 2)
        if average_rating else 0}