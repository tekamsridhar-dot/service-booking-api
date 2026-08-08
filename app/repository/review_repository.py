from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.review import Review
from app.models.booking import Booking
from app.utils.pagination import paginate

def create_review(db: Session, review: Review):
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_review_by_id(db: Session, review_id: int):
    return (
        db.query(Review)
        .filter(Review.id == review_id)
        .first())

def get_review_by_booking(db: Session, booking_id: int):
    return (
        db.query(Review)
        .filter(Review.booking_id == booking_id)
        .first())

def get_provider_reviews(db: Session, provider_id: int):
    return (
        db.query(Review)
        .join(Booking)
        .filter(Booking.provider_id == provider_id)
        .all())

def get_average_rating(db: Session, provider_id: int):
    avg = (
        db.query(func.avg(Review.rating))
        .join(Booking)
        .filter(Booking.provider_id == provider_id)
        .scalar())
    return round(avg, 2) if avg else 0

def update_review(db: Session, review: Review):
    db.commit()
    db.refresh(review)
    return review

def delete_review(db: Session, review: Review):
    review.is_deleted = True
    db.commit()

def provider_reviews(db,provider_id,page=1,size=10,rating=None):
    query = (db.query(Review).join(Booking).filter(
            Booking.provider_id == provider_id))
    if rating:
        query = query.filter(Review.rating == rating)
    query = query.order_by(Review.created_at.desc())
    return paginate(query,page,size)