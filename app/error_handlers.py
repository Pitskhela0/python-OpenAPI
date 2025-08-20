from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from app.exceptions import AppException
import logging


logger = logging.getLogger(__name__)


async def app_exception_handler(request: Request, exc: AppException):
    """Handle custom application exceptions"""
    logger.warning(f"Application error: {exc.message}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "status_code": exc.status_code
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTPException",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    logger.warning(f"Validation error: {exc.errors()}")

    errors = []
    for error in exc.errors():
        field = " -> ".join(str(x) for x in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "message": "Invalid input data",
            "status_code": 422,
            "details": errors
        }
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors"""
    logger.error(f"Database integrity error: {exc}")

    error_message = str(exc.orig)

    if "Duplicate entry" in error_message:
        message = "A record with this ID already exists"
    elif "foreign key constraint" in error_message.lower():
        message = "Referenced record does not exist"
    else:
        message = "Database constraint violation"

    return JSONResponse(
        status_code=409,
        content={
            "error": "IntegrityError",
            "message": message,
            "status_code": 409
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unexpected error: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "status_code": 500
        }
    )
