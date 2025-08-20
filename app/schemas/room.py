from pydantic import BaseModel, Field


class RoomBase(BaseModel):
    room_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=50)


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class RoomResponse(RoomBase):
    class Config:
        from_attributes = True
