from sqlalchemy import (Column,Integer,Date,Time,String,ForeignKey)
from sqlalchemy.orm import relationship
from app.database import Base


class Availability(Base):
    __tablename__ = "availability"
    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer,ForeignKey("users.id"))
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    slot_duration = Column(Integer)
    status = Column(String, default="Available")
    provider = relationship("User",back_populates="availability")