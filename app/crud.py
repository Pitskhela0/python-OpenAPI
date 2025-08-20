"""
Simple CRUD operations for students and rooms with exception handling
"""
from typing import List, Optional, Dict, Any, Type
from sqlalchemy.orm import Session, joinedload
from app.models import Student, Room
from app.schemas import SexEnum
from app.exceptions import (
    RoomNotFoundError,
    StudentNotFoundError,
    RoomAlreadyExistsError,
    StudentAlreadyExistsError,
    RoomHasStudentsError,
    InvalidRoomAssignmentError
)


# ============ ROOM CRUD OPERATIONS ============

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


# ============ STUDENT CRUD OPERATIONS ============

def get_student(db: Session, student_id: int) -> Optional[Student]:
    """Get student by ID"""
    return db.query(Student).filter(Student.student_id == student_id).first()


def get_student_with_room(db: Session, student_id: int) -> Optional[Student]:
    """Get student by ID with room"""
    return (
        db.query(Student)
        .options(joinedload(Student.room))
        .filter(Student.student_id == student_id)
        .first()
    )


def get_students(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
        sex: Optional[SexEnum] = None,
        room_id: Optional[int] = None,
        has_room: Optional[bool] = None
) -> list[Type[Student]]:
    """Get students with optional filtering"""
    query = db.query(Student)

    if name:
        query = query.filter(Student.name.ilike(f"%{name}%"))
    if sex:
        query = query.filter(Student.sex == sex)
    if room_id:
        query = query.filter(Student.room_id == room_id)
    if has_room is not None:
        if has_room:
            query = query.filter(Student.room_id.is_not(None))
        else:
            query = query.filter(Student.room_id.is_(None))

    return query.offset(skip).limit(limit).all()


def create_student(
        db: Session,
        student_id: int,
        name: str,
        birthday,
        sex: SexEnum,
        room_id: Optional[int] = None
) -> Student:
    """Create new student"""
    if student_exists(db, student_id):
        raise StudentAlreadyExistsError(student_id)

    if room_id is not None and not room_exists(db, room_id):
        raise InvalidRoomAssignmentError(room_id)

    db_student = Student(
        student_id=student_id,
        name=name,
        birthday=birthday,
        sex=sex,
        room_id=room_id
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(
        db: Session,
        student_id: int,
        name: Optional[str] = None,
        birthday=None,
        sex: Optional[SexEnum] = None,
        room_id: Optional[int] = None
) -> Student:
    """Update student"""
    db_student = get_student(db, student_id)
    if not db_student:
        raise StudentNotFoundError(student_id)

    if room_id is not None and not room_exists(db, room_id):
        raise InvalidRoomAssignmentError(room_id)

    if name is not None:
        db_student.name = name
    if birthday is not None:
        db_student.birthday = birthday
    if sex is not None:
        db_student.sex = sex
    if room_id is not None:
        db_student.room_id = room_id

    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int) -> Student:
    """Delete student"""
    db_student = get_student(db, student_id)
    if not db_student:
        raise StudentNotFoundError(student_id)

    db.delete(db_student)
    db.commit()
    return db_student


def student_exists(db: Session, student_id: int) -> bool:
    """Check if student exists"""
    return db.query(Student).filter(Student.student_id == student_id).first() is not None


def move_student(db: Session, student_id: int, room_id: Optional[int]) -> Student:
    """Move student to different room (or unassign if room_id is None)"""
    db_student = get_student(db, student_id)
    if not db_student:
        raise StudentNotFoundError(student_id)

    if room_id is not None and not room_exists(db, room_id):
        raise InvalidRoomAssignmentError(room_id)

    db_student.room_id = room_id
    db.commit()
    db.refresh(db_student)
    return db_student


# ============ HELPER FUNCTIONS ============

def count_students(db: Session) -> int:
    """Count total students"""
    return db.query(Student).count()


def count_rooms(db: Session) -> int:
    """Count total rooms"""
    return db.query(Room).count()


def count_students_in_room(db: Session, room_id: int) -> int:
    """Count students in specific room"""
    return db.query(Student).filter(Student.room_id == room_id).count()


def get_unassigned_students(db: Session) -> list[Type[Student]]:
    """Get students not assigned to any room"""
    return db.query(Student).filter(Student.room_id.is_(None)).all()