from sqlalchemy import (Column,Integer,Date,Time,Float,String,ForeignKey,Boolean)
from sqlalchemy.orm import relationship
from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer,ForeignKey("users.id"))
    provider_id = Column(Integer,ForeignKey("users.id"))
    service_id = Column(Integer,ForeignKey("services.id"))
    appointment_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    total_amount = Column(Float)
    status = Column(String,default="Pending")
    is_deleted = Column(Boolean, default=False)
    customer = relationship("User",foreign_keys=[customer_id],back_populates="customer_bookings")
    provider = relationship("User",foreign_keys=[provider_id],back_populates="provider_bookings")
    service = relationship("Service",back_populates="bookings")
    payment = relationship("Payment",back_populates="booking",uselist=False)
    review = relationship("Review",back_populates="booking",uselist=False)