from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    content: str
    room_id: int

class MessageResponse(BaseModel):
    id: int
    content: str
    room_id: int
    sender_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class WebSocketMessage(BaseModel):
    content: str
    room_id: int
    sender_id: int
    username: str
    created_at: str