from sqlalchemy import Column, Integer, String, DateTime,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    profile_image = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
    services = relationship("Service", back_populates="provider")
    availability = relationship( "Availability",back_populates="provider")
    customer_bookings = relationship("Booking",foreign_keys="Booking.customer_id",back_populates="customer")
    provider_bookings = relationship( "Booking",foreign_keys="Booking.provider_id",back_populates="provider")
    notifications = relationship("Notification",back_populates="user")