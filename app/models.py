"""
SQLAlchemy database models
"""
from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class SexEnum(enum.Enum):
    """Enum for student sex"""
    M = "M"
    F = "F"


class Room(Base):
    """Room model"""
    __tablename__ = "Rooms"

    room_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    # Relationship with students
    students = relationship("Student", back_populates="room")


class Student(Base):
    """Student model"""
    __tablename__ = "Students"

    student_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    birthday = Column(Date, nullable=False)
    sex = Column(Enum(SexEnum), nullable=False)
    room_id = Column(Integer, ForeignKey("Rooms.room_id"), nullable=True)

    # Relationship with room
    room = relationship("Room", back_populates="students")