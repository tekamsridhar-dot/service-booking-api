from pydantic import BaseModel, EmailStr
from datetime import date,time

class BookingCreate(BaseModel):
    service_id: int
    provider_id: int
    appointment_date: date
    start_time: time
    end_time: time
    status: str = "pending"

class  BookingResponse(BaseModel):
    id: int
    customer_id: int
    service_id: int
    provider_id: int
    appointment_date: date
    start_time: time
    end_time: time
    total_amount: float
    status: str

    model_config = {"from_attributes": True}