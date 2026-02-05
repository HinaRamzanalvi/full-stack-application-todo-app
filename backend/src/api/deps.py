"""Dependency functions for API endpoints."""

from fastapi import Depends, HTTPException, status
from typing import Generator
from sqlmodel import Session
from database.session import engine
from middleware.auth import get_current_user, TokenData


def get_db_session() -> Generator[Session, None, None]:
    """Dependency to get a database session."""
    with Session(engine) as session:
        yield session


def get_current_active_user(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    """Dependency to get the current active user with validation."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user