"""
Database migration script for creating tables.
This creates all tables defined in the models module.
"""

import sys
import os
# Add the backend root directory to the path so we can import from both models locations
backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, backend_root)

from sqlmodel import SQLModel
from sqlalchemy import create_engine
from database.config import settings

# Import models to register them with SQLModel
from models.task import Task  # Import existing models from backend/models
from models.user import User
from src.models.conversation import Conversation  # Import new models from src/models
from src.models.message import Message

def run_migrations():
    """Run database migrations to create all tables."""
    engine = create_engine(settings.database_url, echo=settings.db_echo_sql)

    # Create all tables defined in SQLModel models
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    run_migrations()