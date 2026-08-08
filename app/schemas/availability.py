from pydantic import BaseModel, EmailStr
from datetime import date,time

class AvailabilityCreate(BaseModel):
    date: date
    start_time: time
    end_time: time
    slot_duration: int 

class AvailabilityUpdate(BaseModel):
    date: date
    start_time: time
    end_time: time
    slot_duration: int 
    status: str
    
class AvailabilityResponse(BaseModel):
    id: int
    provider_id: int
    date: date
    start_time: time
    end_time: time
    slot_duration: int 
    status: str

    model_config = {"from_attributes": True}
