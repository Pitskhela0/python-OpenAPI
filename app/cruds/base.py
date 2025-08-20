from typing import Optional, Type
from sqlalchemy.orm import Session
from app.models import Student, Room
from app.schemas import SexEnum


def count_students(db: Session) -> int:
    """Count total students"""
    return db.query(Student).count()


def count_rooms(db: Session) -> int:
    """Count total rooms"""
    return db.query(Room).count()


def get_unassigned_students(db: Session) -> list[Type[Student]]:
    """Get students not assigned to any room"""
    return db.query(Student).filter(Student.room_id.is_(None)).all()


def count_students_filtered(
        db: Session,
        name: Optional[str] = None,
        sex: Optional[SexEnum] = None,
        room_id: Optional[int] = None,
        has_room: Optional[bool] = None
) -> int:
    """Count students with same filters as get_students"""
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

    return query.count()


def count_rooms_filtered(db: Session) -> int:
    """Count rooms (no filters for now, but keeping consistent pattern)"""
    return db.query(Room).count()
