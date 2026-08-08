from sqlalchemy import Column, Integer, String, Float, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)
    duration = Column(Integer)
    price = Column(Float)
    status = Column(String, default="Active")
    image = Column(String)
    is_deleted = Column(Boolean, default=False)
    provider = relationship("User",back_populates="services")
    bookings = relationship("Booking",back_populates="service")