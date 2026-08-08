from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.repository import review_repository, booking_repository
from app.models.review import Review
from app.schemas.review import (ReviewCreate,ReviewUpdate,ReviewResponse,ProviderReviewResponse)
from app.core.permissions import (require_customer,require_authenticated_user)

router = APIRouter( prefix="/reviews",
                    tags=["Reviews"])

@router.post("",response_model=ReviewResponse)
def create_review(
    request: ReviewCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_customer)):
    booking = booking_repository.get_booking_by_id(db,request.booking_id)
    if not booking:
        raise HTTPException(status_code=404,
                            detail="Booking not found.")
    if booking.customer_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="Access denied.")
    if booking.status != "Completed":
        raise HTTPException(status_code=400,
                            detail="Only completed bookings can be reviewed.")
    existing = review_repository.get_review_by_booking(db,request.booking_id)
    if existing:
        raise HTTPException(status_code=400,
                            detail="Review already submitted.")
    review = Review(
        booking_id=request.booking_id,
        rating=request.rating,
        review=request.review)
    return review_repository.create_review(db,review)

@router.get("/provider/{provider_id}",response_model=ProviderReviewResponse)
def provider_reviews(
    provider_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated_user)):
    reviews = review_repository.get_provider_reviews(db,provider_id)
    average = review_repository.get_average_rating(db,provider_id)
    return {"average_rating": average,
            "total_reviews": len(reviews),
            "reviews": reviews}

@router.put("/{review_id}",response_model=ReviewResponse)
def update_review(
    review_id: int,
    request: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_customer)):
    review = review_repository.get_review_by_id(db,review_id)
    if not review:
        raise HTTPException(status_code=404,
                            detail="Review not found.")
    booking = booking_repository.get_booking_by_id(db,review.booking_id)
    if booking.customer_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="Access denied.")
    review.rating = request.rating
    review.review = request.review
    return review_repository.update_review(db,review)

@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_customer)):
    review = review_repository.get_review_by_id(db,review_id)
    if not review:
        raise HTTPException(status_code=404,
                            detail="Review not found.")
    booking = booking_repository.get_booking_by_id(db,review.booking_id)
    if booking.customer_id != current_user.id:
        raise HTTPException(status_code=403,
                            detail="Access denied.")
    review_repository.delete_review(db,review)
    return {"message": "Review deleted successfully."}