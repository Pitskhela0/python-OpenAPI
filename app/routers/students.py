from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
import app.cruds as crud
from app.schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    StudentWithRoomResponse,
    StudentMoveRequest,
    SexEnum,
    ErrorResponse,
    PaginatedResponse
)

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[StudentResponse],
    summary="Get all students",
    description="Retrieve all students with optional filtering and pagination metadata"
)
async def get_students(
    skip: int = Query(0, ge=0, description="Number of students to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of students to return"),
    name: Optional[str] = Query(None, description="Filter by name (partial match)"),
    sex: Optional[SexEnum] = Query(None, description="Filter by sex (M or F)"),
    room_id: Optional[int] = Query(None, gt=0, description="Filter by room ID"),
    has_room: Optional[bool] = Query(None, description="Filter students with/without room assignment"),
    db: Session = Depends(get_db)
):
    """Get all students with optional filtering and pagination metadata"""

    students = crud.get_students(
        db=db,
        skip=skip,
        limit=limit,
        name=name,
        sex=sex,
        room_id=room_id,
        has_room=has_room
    )

    total = crud.count_students_filtered(
        db=db,
        name=name,
        sex=sex,
        room_id=room_id,
        has_room=has_room
    )

    pages = (total + limit - 1) // limit if total > 0 else 0
    page = (skip // limit) + 1

    return PaginatedResponse[StudentResponse](
        data=students,
        total=total,
        page=page,
        size=limit,
        pages=pages
    )


@router.get(
    "/{student_id}",
    response_model=StudentWithRoomResponse,
    summary="Get student by ID",
    description="Retrieve a specific student by ID with room information",
    responses={
        404: {"model": ErrorResponse, "description": "Student not found"}
    }
)
async def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific student by ID with room information"""
    student = crud.get_student_with_room(db, student_id)
    if not student:
        from app.exceptions import StudentNotFoundError
        raise StudentNotFoundError(student_id)
    return student


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=201,
    summary="Create new student",
    description="Create a new student",
    responses={
        201: {"description": "Student created successfully"},
        409: {"model": ErrorResponse, "description": "Student with this ID already exists"},
        400: {"model": ErrorResponse, "description": "Invalid room assignment"},
        422: {"model": ErrorResponse, "description": "Validation error"}
    }
)
async def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    """Create a new student"""
    return crud.create_student(
        db=db,
        student_id=student.student_id,
        name=student.name,
        birthday=student.birthday,
        sex=student.sex,
        room_id=student.room_id
    )


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Update student",
    description="Update an existing student",
    responses={
        404: {"model": ErrorResponse, "description": "Student not found"},
        400: {"model": ErrorResponse, "description": "Invalid room assignment"},
        422: {"model": ErrorResponse, "description": "Validation error"}
    }
)
async def update_student(
    student_id: int,
    student_update: StudentUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing student"""
    return crud.update_student(
        db=db,
        student_id=student_id,
        name=student_update.name,
        birthday=student_update.birthday,
        sex=student_update.sex,
        room_id=student_update.room_id
    )


@router.delete(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Delete student",
    description="Delete a student",
    responses={
        404: {"model": ErrorResponse, "description": "Student not found"}
    }
)
async def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Delete a student"""
    return crud.delete_student(db, student_id)


@router.patch(
    "/{student_id}/move",
    response_model=StudentResponse,
    summary="Move student to different room",
    description="Move a student to a different room or unassign from room",
    responses={
        404: {"model": ErrorResponse, "description": "Student not found"},
        400: {"model": ErrorResponse, "description": "Invalid room assignment"}
    }
)
async def move_student(
    student_id: int,
    move_request: StudentMoveRequest,
    db: Session = Depends(get_db)
):
    """Move a student to a different room or unassign from room"""
    return crud.move_student(db, student_id, move_request.room_id)