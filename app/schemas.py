"""
Simple Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum


class SexEnum(str, Enum):
    """Sex enumeration"""
    M = "M"
    F = "F"


# ============ ROOM SCHEMAS ============

class RoomBase(BaseModel):
    room_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=50)


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class RoomResponse(RoomBase):
    class Config:
        from_attributes = True


class RoomWithStudentsResponse(RoomResponse):
    students: List['StudentResponse'] = []


# ============ STUDENT SCHEMAS ============

class StudentBase(BaseModel):
    student_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=50)
    birthday: date
    sex: SexEnum
    room_id: Optional[int] = Field(None, gt=0)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    birthday: Optional[date] = None
    sex: Optional[SexEnum] = None
    room_id: Optional[int] = Field(None, gt=0)


class StudentMoveRequest(BaseModel):
    room_id: Optional[int] = Field(None, gt=0)


class StudentResponse(StudentBase):
    class Config:
        from_attributes = True


class StudentWithRoomResponse(StudentResponse):
    room: Optional[RoomResponse] = None


# ============ ERROR SCHEMAS ============

class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int


# ============ PAGINATION SCHEMAS ============

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)


class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    size: int
    pages: int


# Fix forward references
RoomWithStudentsResponse.model_rebuild()
StudentWithRoomResponse.model_rebuild()