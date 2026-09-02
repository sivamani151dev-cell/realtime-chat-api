from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.Message import Message
from app.models.Room import RoomMember
from app.models.user import User
from app.schemas.message import MessageResponse
from app.auth import decode_access_token
from app.websocket import manager
from app.cache import publish_message, subscribe_to_channel
from fastapi.security import OAuth2PasswordBearer
import asyncio
import json

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
    user_id: int = Depends(get_current_user_id)):
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

@router.websocket("/ws/{room_id}/{token}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: int,
    token: str,
    db: Session = next(get_db())
):
    # Authenticate user
    payload = decode_access_token(token)
    if not payload:
        await websocket.close(code=1008)
        return

    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        await websocket.close(code=1008)
        return

    # Check room membership
    member = db.query(RoomMember).filter(
        RoomMember.room_id == room_id,
        RoomMember.user_id == user_id
    ).first()
    if not member:
        await websocket.close(code=1008)
        return

    # Connect to room
    await manager.connect(websocket, room_id)

    # Subscribe to Redis channel
    channel = f"room:{room_id}"
    pubsub, redis = await subscribe_to_channel(channel)

    try:
        async def listen_redis():
            async for redis_message in pubsub.listen():
                if redis_message["type"] == "message":
                    data = json.loads(redis_message["data"])
                    await manager.send_message_to_room(data, room_id)

        redis_task = asyncio.create_task(listen_redis())

        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Save to DB
            new_message = Message(
                content=message_data["content"],
                room_id=room_id,
                sender_id=user_id
            )
            db.add(new_message)
            db.commit()
            db.refresh(new_message)

            # Publish to Redis
            payload_msg = {
                "id": new_message.id,
                "content": new_message.content,
                "room_id": room_id,
                "sender_id": user_id,
                "username": user.username,
                "created_at": str(new_message.created_at)
            }
            await publish_message(channel, payload_msg)

    except WebSocketDisconnect:
        redis_task.cancel()
        await pubsub.unsubscribe(channel)
        await redis.close()
        manager.disconnect(websocket, room_id)