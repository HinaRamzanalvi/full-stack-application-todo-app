import sys
import os

# Add the src directory to the Python path to resolve imports correctly
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.session import engine
# Import models to register them with SQLAlchemy's metadata
from models.user import User
from models.task import Task
from src.models.conversation import Conversation  # Add conversation model
from src.models.message import Message  # Add message model
from database.config import settings
from sqlmodel import SQLModel


# --- Application Setup ---
app = FastAPI(
    title="Production Todo API",
    version="1.0.0",
)

# --- CORS Middleware ---
# This allows your frontend (running on a different domain) to communicate
# with your backend. Now configured for production with specific origins.
origins = [
    "https://your-vercel-project.vercel.app",  # Replace with your actual Vercel URL
    "http://localhost:3000",                   # For local development
    "http://localhost:3001",                   # Alternative local port
    "http://127.0.0.1:3000",                   # Alternative local IP
    "http://127.0.0.1:3001",                   # Alternative local IP
    # Add your actual Vercel URL here after deployment
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
    allow_headers=["*"],
)

# --- Database Initialization ---
def init_db():
    """
    Initializes the database. In a production environment, you would use
    Alembic migrations instead of `create_all`.
    """
    try:
        # This creates tables for all models that inherit from `Base`.
        print("Initializing database and creating tables...")
        SQLModel.metadata.create_all(bind=engine)
        print("Database initialization complete.")
    except Exception as e:
        print(f"An error occurred during database initialization: {e}")
        # Continue without raising the exception to allow the app to start
        # This allows the app to start even if there are initial DB issues
        # The individual endpoints will handle DB errors appropriately
        pass

from api.routes import auth, tasks
from src.api.routes.chat import router as chat_router

# Include the routers
app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(tasks.router, prefix="", tags=["tasks"])
app.include_router(chat_router, prefix="", tags=["chat"])

@app.on_event("startup")
def on_startup():
    init_db()

# --- API Endpoints ---
@app.get("/", tags=["Health Check"])
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)  # Changed to port 8001