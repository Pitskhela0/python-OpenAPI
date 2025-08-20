"""
CRUD operations package - centralized imports
"""

from .base import (
    count_students,
    count_rooms,
    get_unassigned_students
)

from .room import (
    get_room,
    get_room_with_students,
    get_rooms,
    create_room,
    update_room,
    delete_room,
    room_exists,
    room_has_students,
    get_students_in_room,
    count_students_in_room
)

from .student import (
    get_student,
    get_student_with_room,
    get_students,
    create_student,
    update_student,
    delete_student,
    student_exists,
    move_student
)

__all__ = [
    "count_students",
    "count_rooms",
    "get_unassigned_students",

    "get_room",
    "get_room_with_students",
    "get_rooms",
    "create_room",
    "update_room",
    "delete_room",
    "room_exists",
    "room_has_students",
    "get_students_in_room",
    "count_students_in_room",

    "get_student",
    "get_student_with_room",
    "get_students",
    "create_student",
    "update_student",
    "delete_student",
    "student_exists",
    "move_student"
]
