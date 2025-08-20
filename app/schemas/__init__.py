"""
Schemas package - centralized imports
"""

from .base import SexEnum, ErrorResponse

from .room import (
    RoomBase,
    RoomCreate,
    RoomUpdate,
    RoomResponse
)

from .student import (
    StudentBase,
    StudentCreate,
    StudentUpdate,
    StudentMoveRequest,
    StudentResponse,
    StudentWithRoomResponse
)

from .pagination import (
    PaginationParams,
    PaginatedResponse
)

__all__ = [
    "SexEnum",
    "ErrorResponse",

    "RoomBase",
    "RoomCreate",
    "RoomUpdate",
    "RoomResponse",

    "StudentBase",
    "StudentCreate",
    "StudentUpdate",
    "StudentMoveRequest",
    "StudentResponse",
    "StudentWithRoomResponse",

    "PaginationParams",
    "PaginatedResponse"
]
