from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from .base import SexEnum
from .room import RoomResponse


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
    room: Optional['RoomResponse'] = None


StudentWithRoomResponse.model_rebuild()
