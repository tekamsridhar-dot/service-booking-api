from sqlalchemy import (Column,Integer,Float,String,DateTime,ForeignKey)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer,ForeignKey("bookings.id"),unique=True)
    amount = Column(Float)
    payment_method = Column(String)
    payment_status = Column(String,default="Pending")
    payment_date = Column(DateTime,default=datetime.utcnow)
    booking = relationship("Booking",back_populates="payment")
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)