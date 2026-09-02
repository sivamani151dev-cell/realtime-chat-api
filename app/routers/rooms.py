from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.room import Room, RoomMember
from app.schemas.room import RoomCreate, RoomResponse, RoomMemberResponse
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/rooms", tags=["Rooms"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return int(payload.get("sub"))

@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    existing = db.query(Room).filter(Room.name == room.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room name already exists"
        )
    new_room = Room(
        name=room.name,
        description=room.description,
        is_private=room.is_private
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    # Auto join creator
    member = RoomMember(room_id=new_room.id, user_id=user_id)
    db.add(member)
    db.commit()

    return new_room

@router.get("/", response_model=List[RoomResponse])
def get_rooms(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return db.query(Room).filter(Room.is_private == False).all()

@router.post("/{room_id}/join", response_model=RoomMemberResponse)
def join_room(
    room_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    existing = db.query(RoomMember).filter(
        RoomMember.room_id == room_id,
        RoomMember.user_id == user_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already a member"
        )
    member = RoomMember(room_id=room_id, user_id=user_id)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

@router.get("/{room_id}/members", response_model=List[RoomMemberResponse])
def get_room_members(
    room_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return db.query(RoomMember).filter(RoomMember.room_id == room_id).all()