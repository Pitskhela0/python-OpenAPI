"""
FastAPI application main module
"""
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.database import init_db

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "Student Room Management API"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="A REST API for managing students and rooms",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Student Room Management API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Router imports will be added in later parts
# from app.routers import students, rooms
# app.include_router(students.router, prefix="/students", tags=["students"])
# app.include_router(rooms.router, prefix="/rooms", tags=["rooms"])