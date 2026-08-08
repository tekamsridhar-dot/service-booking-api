from pydantic import BaseModel
from datetime import datetime

class NotificationCreate(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    is_read: bool
    created_at: datetime
    model_config = {"from_attributes": True}

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    is_read: bool
    created_at: datetime
    model_config = {"from_attributes": True}