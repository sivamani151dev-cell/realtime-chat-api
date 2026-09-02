from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, rooms, chat

app = FastAPI(
    title="Real-time Chat API",
    description="WebSocket-based real-time chat with Redis Pub/Sub, FastAPI and PostgreSQL",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {
        "message": "Real-time Chat API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}