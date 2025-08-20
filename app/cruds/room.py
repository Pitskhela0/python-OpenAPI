from typing import Optional, Type
from sqlalchemy.orm import Session, joinedload
from app.models import Room, Student
from app.exceptions import (
    RoomNotFoundError,
    RoomAlreadyExistsError,
    RoomHasStudentsError
)


def get_room(db: Session, room_id: int) -> Optional[Room]:
    """Get room by ID"""
    return db.query(Room).filter(Room.room_id == room_id).first()


def get_room_with_students(db: Session, room_id: int) -> Optional[Room]:
    """Get room by ID with students"""
    return (
        db.query(Room)
        .options(joinedload(Room.students))
        .filter(Room.room_id == room_id)
        .first()
    )


def get_rooms(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Room]]:
    """Get all rooms"""
    return db.query(Room).offset(skip).limit(limit).all()


def create_room(db: Session, room_id: int, name: str) -> Room:
    """Create new room"""
    # Check if room already exists
    if room_exists(db, room_id):
        raise RoomAlreadyExistsError(room_id)

    db_room = Room(room_id=room_id, name=name)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def update_room(db: Session, room_id: int, name: str) -> Room:
    """Update room"""
    db_room = get_room(db, room_id)
    if not db_room:
        raise RoomNotFoundError(room_id)

    db_room.name = name
    db.commit()
    db.refresh(db_room)
    return db_room


def delete_room(db: Session, room_id: int) -> Room:
    """Delete room"""
    db_room = get_room(db, room_id)
    if not db_room:
        raise RoomNotFoundError(room_id)

    # Check if room has students
    student_count = count_students_in_room(db, room_id)
    if student_count > 0:
        raise RoomHasStudentsError(room_id, student_count)

    db.delete(db_room)
    db.commit()
    return db_room


def room_exists(db: Session, room_id: int) -> bool:
    """Check if room exists"""
    return db.query(Room).filter(Room.room_id == room_id).first() is not None


def room_has_students(db: Session, room_id: int) -> bool:
    """Check if room has students"""
    return db.query(Student).filter(Student.room_id == room_id).first() is not None


def get_students_in_room(db: Session, room_id: int) -> list[Type[Student]]:
    """Get all students in a room"""
    return db.query(Student).filter(Student.room_id == room_id).all()


def count_students_in_room(db: Session, room_id: int) -> int:
    """Count students in specific room"""
    return db.query(Student).filter(Student.room_id == room_id).count()
