from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from app.core.exception_handler import (validation_exception_handler)
from app.core.logging import LoggingMiddleware
from app.routers import auth,service,availability,booking,payments,review,notification,dashboard,upload,export

app = FastAPI(title="Service Booking & Appointment Management API",
              description="""This API allows users to book services and manage appointments efficiently.
              <br><br><b>Created by:</b> Sridhar Tekam""",)

app.include_router(auth.router)
app.include_router(service.router)
app.include_router(availability.router)
app.include_router(booking.router)
app.include_router(payments.router)
app.include_router(review.router)
app.include_router(notification.router)
app.include_router(dashboard.router)
app.include_router(upload.router)
app.include_router(export.router)
app.add_middleware(LoggingMiddleware)
app.add_exception_handler(RequestValidationError,validation_exception_handler)

app.mount("/uploads",StaticFiles(directory="uploads"),
                                name="uploads")

@app.get("/")
def root():
    return{"message": "Welcome to the Service Booking & Appointment Management API!"}

