from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
from app.controllers import auth_controller, chat_controller, document_controller, user_controller
from app.database.base import engine, Base
from app.database.init_db import init_database

# Load environment variables
load_dotenv()

# Import all models to ensure they are registered with SQLAlchemy
from app.models import User, Conversation, Message, UserDocument, ContactMessage

# Initialize database
init_database()

# Create database tables
Base.metadata.create_all(bind=engine)

# Startup event to initialize global instances
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize global instances when FastAPI starts"""
    from app.core.global_instances import initialize_global_instances, is_initialized
    from app.core.globals import preprocessing_instance
    
    if not is_initialized():
        print("🔄 Starting global instances initialization...")
        initialize_global_instances()
    else:
        print("✅ Global instances already initialized, skipping...")
    
    print("✅ PreProcessing singleton initialized successfully")
    print("🚀 FastAPI server startup completed!")
    
    yield
    
    # Cleanup code can go here if needed
    print("🔄 FastAPI server shutting down...")

# Create FastAPI app with lifespan
app = FastAPI(title="Chatbot API", version="1.0.0", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
)

# Add logging middleware
from app.middleware.logging_middleware import LoggingMiddleware
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(auth_controller.router)
app.include_router(chat_controller.router)
app.include_router(document_controller.router)
app.include_router(user_controller.router)

@app.get("/")
def root():
    return {"message": "Chatbot API is running"}

@app.get("/health")
def health():
    return {"status": "OK", "message": "Server is running"}

@app.get("/status/global-instances")
def global_instances_status():
    """Check the status of global instances"""
    from app.core.global_instances import get_initialization_status
    return get_initialization_status()

# Handle preflight requests
@app.options("/{full_path:path}")
def options_handler(full_path: str):
    return {"message": "OK"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        timeout_keep_alive=1200,  # 20 minutes keep-alive timeout
        timeout_graceful_shutdown=30  # 30 seconds graceful shutdown
    )