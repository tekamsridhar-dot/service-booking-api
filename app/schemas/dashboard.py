from pydantic import BaseModel

class AdminDashboardResponse(BaseModel):
    total_users: int
    total_providers: int
    total_services: int
    total_bookings: int
    completed_bookings: int
    cancelled_bookings: int
    total_revenue: float

class ProviderDashboardResponse(BaseModel):
    today_appointments:int
    upcoming_appointments:int
    completed_appointments:int
    total_earnings:float
    average_rating:float
