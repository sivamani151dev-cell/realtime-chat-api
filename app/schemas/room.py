from pydantic import BaseModel
from datetime import datetime

class RoomCreate(BaseModel):
    name: str
    description: str | None = None
    is_private: bool = False

class RoomResponse(BaseModel):
    id: int
    name: str
    description: str | None
    is_private: bool
    created_at: datetime

    class Config:
        from_attributes = True

class RoomMemberResponse(BaseModel):
    id: int
    room_id: int
    user_id: int
    joined_at: datetime

    class Config:
        from_attributes = True