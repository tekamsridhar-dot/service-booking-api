# Service Booking API

A RESTful backend application built with **FastAPI** for managing service bookings. The system provides secure authentication, role-based authorization, service management, appointment booking, availability scheduling, payments, reviews, notifications, dashboard analytics, image uploads, CSV exports, and Docker-based deployment.

---

# Features

* JWT Authentication
* Role-Based Access Control (RBAC)
* User Registration & Login
* Service Management (CRUD)
* Provider Availability Management
* Appointment Booking
* Booking Confirmation & Rescheduling
* Booking History
* Payment Management
* Customer Reviews & Ratings
* Notifications
* Dashboard Analytics
* Image Upload
* CSV Export
* Search, Filtering & Pagination
* Swagger API Documentation
* Alembic Database Migrations
* Docker & Docker Compose Support

---

# Technology Stack

* Python 3.x
* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* Alembic
* Pydantic
* JWT Authentication
* Passlib (Password Hashing)
* Docker
* Docker Compose
* Uvicorn

---

# Project Structure

```text
service-booking-api/
│
├── app/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── repository/
│   ├── services/
│   ├── routers/
│   ├── utils/
│   ├── dependencies.py
│   ├── database.py
│   └── main.py
│
├── alembic/
├── screenshots/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Project Modules

## Authentication

* User Registration
* User Login
* JWT Token Generation
* Password Hashing
* Password Change
* User Profile

---

## Role-Based Access Control (RBAC)

Supported Roles:

* Admin
* Service Provider
* Customer

Permissions are enforced using FastAPI dependencies.

---

## Service Management

* Create Service
* View Services
* Update Service
* Delete Service
* Upload Service Image

---

## Availability Management

Service providers can:

* Create Availability
* Update Availability
* View Availability

---

## Booking Management

* Book Appointment
* Booking History
* Booking Details
* Confirm Booking
* Reschedule Booking
* Cancel Booking

---

## Payment Management

* Create Payment
* Refund Payment
* Payment History
* Payment Status Tracking

---

## Review Management

* Add Review
* Update Review
* Delete Review
* Provider Reviews

---

## Notifications

* Get Notifications
* Mark Notification as Read
* Mark All Notifications as Read
* Pagination Support

---

## Dashboard

Dashboard APIs provide:

* Total Services
* Total Bookings
* Active Customers
* Revenue Summary
* Provider Statistics

---

## CSV Export

Export data as CSV:

* Bookings
* Customers
* Services

---

## Image Upload

* Upload Service Images
* Image Validation
* Unique File Names
* Static File Serving

---

# API Documentation

After running the project, API documentation is available at:

**Swagger UI**

```text
http://127.0.0.1:8000/docs
```

**ReDoc**

```text
http://127.0.0.1:8000/redoc
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/tekamsridhar-dot/service-booking-api.git
cd service-booking-api
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file and configure your application settings.


## 5. Run Database Migrations

```bash
alembic upgrade head
```

---

## 6. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8001
```

---

# Running with Docker

Build and start the containers:

```bash
docker-compose up --build
```

Stop the containers:

```bash
docker-compose down
```

---

# Testing

The APIs can be tested using:

* Swagger UI
* Postman

---

# Repository Pattern

The project follows the Repository Pattern to separate database access from business logic.

Benefits:

* Cleaner Code
* Reusable Database Operations
* Easier Unit Testing
* Better Maintainability

---

# Security

* JWT Authentication
* Password Hashing with Passlib
* Role-Based Authorization
* Input Validation using Pydantic
* Centralized Exception Handling

---

# Screenshots

The `screenshots/` directory contains sample API responses and Swagger UI screenshots for major modules.

---

# Future Enhancements

* Email Verification
* SMS Notifications
* Payment Gateway Integration
* Redis Caching
* API Rate Limiting
* CI/CD Pipeline
* Kubernetes Deployment

---

# Author

**Sridhar Tekam**

Backend Developer | Python | FastAPI | PostgreSQL | SQLAlchemy

