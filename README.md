# Real-time Chat API 🚀

A production-ready real-time chat backend built with 
FastAPI, WebSockets, Redis Pub/Sub, and PostgreSQL.

## 🔴 Live Demo
**API Docs:** [coming soon after deploy]

## 🛠️ Tech Stack
| Technology | Purpose |
|------------|---------|
| Python 3.11 | Programming language |
| FastAPI | Web framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Alembic | Migrations |
| Redis | Pub/Sub messaging |
| WebSockets | Real-time communication |
| Docker | Containerization |
| JWT | Authentication |

## ✨ Features
- Real-time messaging with WebSockets
- Redis Pub/Sub for message broadcasting
- JWT authentication
- Public and private chat rooms
- Room membership management
- Message history
- Auto-redirect to Swagger UI

## 🚀 How To Run

### Without Docker:
```bash
git clone https://github.com/sivamani151dev-cell/realtime-chat-api.git
cd realtime-chat-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m alembic upgrade head
uvicorn app.main:app --reload
```

### With Docker:
```bash
docker-compose up --build
```

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Register user | ❌ |
| POST | `/auth/login` | Login + get token | ❌ |

### Rooms
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/rooms/` | Create room | ✅ |
| GET | `/rooms/` | List public rooms | ✅ |
| POST | `/rooms/{id}/join` | Join room | ✅ |
| GET | `/rooms/{id}/members` | Get members | ✅ |

### Chat
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/chat/{id}/messages` | Get messages | ✅ |
| WS | `/chat/ws/{room_id}/{token}` | WebSocket chat | ✅ |

## 🔌 WebSocket Usage

Connect: ws://your-url/chat/ws/{room_id}/{jwt_token}

Send message:
{"content": "Hello World!"}

Receive message:
{
"id": 1,
"content": "Hello World!",
"room_id": 1,
"sender_id": 1,
"username": "sivamani",
"created_at": "2026-09-02T13:42:11"
}


## 🎯 Project Type
Production-ready real-time chat backend — 
demonstrates WebSockets, Redis Pub/Sub, 
JWT auth, and scalable room management.