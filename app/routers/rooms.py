from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
import app.cruds as crud
from app.schemas import (
    RoomCreate,
    RoomUpdate,
    RoomResponse,
    StudentResponse,
    ErrorResponse,
    PaginatedResponse
)

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[RoomResponse],
    summary="Get all rooms",
    description="Retrieve all rooms with pagination metadata"
)
async def get_rooms(
        skip: int = Query(0, ge=0, description="Number of rooms to skip"),
        limit: int = Query(10, ge=1, le=100, description="Maximum number of rooms to return"),
        db: Session = Depends(get_db)
):
    """Get all rooms with pagination metadata"""

    rooms = crud.get_rooms(db, skip=skip, limit=limit)

    total = crud.count_rooms_filtered(db)

    pages = (total + limit - 1) // limit if total > 0 else 0
    page = (skip // limit) + 1

    return PaginatedResponse[RoomResponse](
        data=rooms,
        total=total,
        page=page,
        size=limit,
        pages=pages
    )


@router.get(
    "/{room_id}",
    response_model=RoomResponse,
    summary="Get room by ID",
    description="Retrieve a specific room by ID",
    responses={
        404: {"model": ErrorResponse, "description": "Room not found"}
    }
)
async def get_room(
        room_id: int,
        db: Session = Depends(get_db)
):
    """Get a specific room by ID"""
    room = crud.get_room(db, room_id)
    if not room:
        from app.exceptions import RoomNotFoundError
        raise RoomNotFoundError(room_id)
    return room


@router.get(
    "/{room_id}/students",
    response_model=PaginatedResponse[StudentResponse],
    summary="Get students in room",
    description="Get all students assigned to a specific room with pagination metadata",
    responses={
        404: {"model": ErrorResponse, "description": "Room not found"}
    }
)
async def get_students_in_room(
        room_id: int,
        skip: int = Query(0, ge=0, description="Number of students to skip"),
        limit: int = Query(10, ge=1, le=100, description="Maximum number of students to return"),
        db: Session = Depends(get_db)
):
    """Get all students in a specific room with pagination metadata"""
    if not crud.room_exists(db, room_id):
        from app.exceptions import RoomNotFoundError
        raise RoomNotFoundError(room_id)

    all_students = crud.get_students_in_room(db, room_id)
    total = len(all_students)

    students = all_students[skip:skip + limit]

    pages = (total + limit - 1) // limit if total > 0 else 0
    page = (skip // limit) + 1

    return PaginatedResponse[StudentResponse](
        data=students,
        total=total,
        page=page,
        size=limit,
        pages=pages
    )


@router.post(
    "/",
    response_model=RoomResponse,
    status_code=201,
    summary="Create new room",
    description="Create a new room",
    responses={
        201: {"description": "Room created successfully"},
        409: {"model": ErrorResponse, "description": "Room with this ID already exists"},
        422: {"model": ErrorResponse, "description": "Validation error"}
    }
)
async def create_room(
        room: RoomCreate,
        db: Session = Depends(get_db)
):
    """Create a new room"""
    return crud.create_room(
        db=db,
        room_id=room.room_id,
        name=room.name
    )


@router.put(
    "/{room_id}",
    response_model=RoomResponse,
    summary="Update room",
    description="Update an existing room",
    responses={
        404: {"model": ErrorResponse, "description": "Room not found"},
        422: {"model": ErrorResponse, "description": "Validation error"}
    }
)
async def update_room(
        room_id: int,
        room_update: RoomUpdate,
        db: Session = Depends(get_db)
):
    """Update an existing room"""
    return crud.update_room(
        db=db,
        room_id=room_id,
        name=room_update.name
    )


@router.delete(
    "/{room_id}",
    response_model=RoomResponse,
    summary="Delete room",
    description="Delete a room (only if no students are assigned)",
    responses={
        404: {"model": ErrorResponse, "description": "Room not found"},
        400: {"model": ErrorResponse, "description": "Room has students assigned"}
    }
)
async def delete_room(
        room_id: int,
        db: Session = Depends(get_db)
):
    """Delete a room (only if no students are assigned)"""
    return crud.delete_room(db, room_id)
