from typing import Generator
from sqlmodel import Session
from fastapi import Depends, HTTPException
from database.session import SessionLocal
from middleware.auth import get_current_user, TokenData

def get_db_session() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Re-export the current user dependency
current_user = get_current_user
get_current_active_user = get_current_user