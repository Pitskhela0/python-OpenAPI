from pydantic import BaseModel
from enum import Enum


class SexEnum(str, Enum):
    """Sex enumeration"""
    M = "M"
    F = "F"


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    message: str
    status_code: int
