class AppException(Exception):
    """Base application exception"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppException):
    """Raised when a resource is not found"""
    def __init__(self, resource: str, identifier: str):
        message = f"{resource} with id '{identifier}' not found"
        super().__init__(message, 404)


class ConflictError(AppException):
    """Raised when there's a conflict (e.g., duplicate IDs)"""
    def __init__(self, message: str):
        super().__init__(message, 409)


class ValidationError(AppException):
    """Raised when validation fails"""
    def __init__(self, message: str):
        super().__init__(message, 422)


class BusinessLogicError(AppException):
    """Raised when business logic rules are violated"""
    def __init__(self, message: str):
        super().__init__(message, 400)


class RoomNotFoundError(NotFoundError):
    """Raised when room is not found"""
    def __init__(self, room_id: int):
        super().__init__("Room", str(room_id))


class StudentNotFoundError(NotFoundError):
    """Raised when student is not found"""
    def __init__(self, student_id: int):
        super().__init__("Student", str(student_id))


class RoomAlreadyExistsError(ConflictError):
    """Raised when trying to create a room with existing ID"""
    def __init__(self, room_id: int):
        super().__init__(f"Room with id '{room_id}' already exists")


class StudentAlreadyExistsError(ConflictError):
    """Raised when trying to create a student with existing ID"""
    def __init__(self, student_id: int):
        super().__init__(f"Student with id '{student_id}' already exists")


class RoomHasStudentsError(BusinessLogicError):
    """Raised when trying to delete a room that has students"""
    def __init__(self, room_id: int, student_count: int):
        super().__init__(
            f"Cannot delete room '{room_id}'. It has {student_count} student(s) assigned. "
            f"Please move or remove students first."
        )


class InvalidRoomAssignmentError(BusinessLogicError):
    """Raised when trying to assign student to non-existent room"""
    def __init__(self, room_id: int):
        super().__init__(f"Cannot assign student to room '{room_id}'. Room does not exist.")
