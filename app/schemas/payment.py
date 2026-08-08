from pydantic import BaseModel
from datetime import datetime

class PaymentCreate(BaseModel):
    booking_id:int
    payment_method:str

class PaymentResponse(BaseModel):
    id:int
    booking_id:int
    payment_method:str
    amount:float
    payment_status:str
    payment_date:datetime

    model_config = {"from_attributes": True}

    