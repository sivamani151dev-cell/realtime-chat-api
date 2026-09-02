from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers.rooms import router as rooms_router
from app.routers.chat import router as chat_router

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
app.include_router(auth_router)
app.include_router(rooms_router)
app.include_router(chat_router)

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