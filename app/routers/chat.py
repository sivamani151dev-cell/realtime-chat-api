from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.Message import Message
from app.models.Room import RoomMember
from app.schemas.message import MessageResponse
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/chat", tags=["Chat"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return int(payload.get("sub"))

@router.get("/{room_id}/messages", response_model=List[MessageResponse])
def get_messages(
    room_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Check if user is member
    member = db.query(RoomMember).filter(
        RoomMember.room_id == room_id,
        RoomMember.user_id == user_id
    ).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this room"
        )
    messages = db.query(Message).filter(
        Message.room_id == room_id
    ).order_by(Message.created_at.asc()).all()
    return messages