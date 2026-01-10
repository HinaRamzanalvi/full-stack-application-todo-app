from sqlmodel import SQLModel, Field, Column
from typing import Optional
from passlib.context import CryptContext
import uuid
from datetime import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None


class User(UserBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: str
    created_at: datetime


class UserLogin(SQLModel):
    email: str
    password: str


class UserUpdate(SQLModel):
    name: Optional[str] = None