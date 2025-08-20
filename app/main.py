import os
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

from app.database import init_db
from app.exceptions import AppException
from app.error_handlers import (
    app_exception_handler,
    validation_exception_handler,
    integrity_error_handler,
    general_exception_handler
)
from app.routers import students, rooms

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "Student Room Management API"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="A REST API for managing students and rooms with CRUD operations",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, general_exception_handler)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Student Room Management API",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "students": "/students",
            "rooms": "/rooms"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Student Room Management API"
    }


app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(rooms.router, prefix="/rooms", tags=["Rooms"])