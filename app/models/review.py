from sqlalchemy import (Column,Integer,String,DateTime,ForeignKey,Boolean)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer,ForeignKey("bookings.id"),unique=True)
    rating = Column(Integer)
    review = Column(String)
    created_at = Column(DateTime,default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
    booking = relationship("Booking",back_populates="review")