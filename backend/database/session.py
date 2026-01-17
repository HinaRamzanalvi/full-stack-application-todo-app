import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from pydantic import Field

# --- Configuration ---
# Use Pydantic's BaseSettings to read from environment variables.
# This provides strong typing and validation for your settings.
class DBSettings(BaseSettings):
    # The `Field` with `...` makes this a required environment variable.
    # The application will fail to start if this is not set in the environment.
    database_url: str = Field(..., alias='DATABASE_URL')

    class Config:
        # Load from a .env file for local development (optional)
        env_file = ".env"
        # Allow reading variables from the environment
        extra = "ignore"

# Instantiate settings
db_settings = DBSettings()

# --- Database Engine & Session ---
# The engine is the starting point for any SQLAlchemy application.
# It's configured once for the entire application.
# `pool_pre_ping=True` checks connection validity before use, preventing errors
# with disconnected sessions.
engine = create_engine(db_settings.database_url, pool_pre_ping=True)

# SessionLocal is a factory for creating new database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Dependency for FastAPI ---
# This function will be used as a dependency in your API routes.
# It ensures that a database session is created for each request and
# is properly closed afterward, even if an error occurs.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
