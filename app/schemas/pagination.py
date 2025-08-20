from pydantic import BaseModel, Field, computed_field
from typing import List, TypeVar, Generic

T = TypeVar('T')


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response with metadata"""
    data: List[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")

    @computed_field
    @property
    def has_next(self) -> bool:
        """Whether there is a next page"""
        return self.page < self.pages

    @computed_field
    @property
    def has_prev(self) -> bool:
        """Whether there is a previous page"""
        return self.page > 1
