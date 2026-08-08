from pydantic import BaseModel, EmailStr
from typing import Optional

class ServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    duration: int  # Duration in minutes
    price: float
    status:str="active"

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    duration: Optional[int] = None 
    price: Optional[float] = None
    status: Optional[str] = None

class ServiceResponse(BaseModel):
    id: int
    provider_id: int
    name: str
    description: Optional[str]
    category: str
    duration: int 
    price: float
    status:str
    image:Optional[str] = None
    model_config = {"from_attributes": True}