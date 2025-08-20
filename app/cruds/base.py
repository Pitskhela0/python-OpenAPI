from typing import Type
from sqlalchemy.orm import Session
from app.models import Student, Room


def count_students(db: Session) -> int:
    """Count total students"""
    return db.query(Student).count()


def count_rooms(db: Session) -> int:
    """Count total rooms"""
    return db.query(Room).count()


def get_unassigned_students(db: Session) -> list[Type[Student]]:
    """Get students not assigned to any room"""
    return db.query(Student).filter(Student.room_id.is_(None)).all()
