from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional

class ReviewCreate(BaseModel):
    booking_id: int
    rating: int = Field(..., ge=1, le=5)
    review: Optional[str] = None

class ReviewUpdate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    review: Optional[str] = None

class ReviewResponse(BaseModel):
    id: int
    booking_id: int
    rating: int
    review: Optional[str]
    created_at: datetime
    model_config = {"from_attributes": True}

class ProviderReviewResponse(BaseModel):
    average_rating: float
    total_reviews: int
    reviews: list[ReviewResponse]