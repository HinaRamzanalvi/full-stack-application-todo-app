"""Conversation model for chatbot functionality."""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from .message import Message


class ConversationBase(SQLModel):
    """Base class for Conversation model with common fields."""
    user_id: str = Field(index=True, nullable=False, description="ID of the user who owns this conversation")
    title: Optional[str] = Field(default=None, description="Optional title for the conversation")


class Conversation(ConversationBase, table=True):
    """Conversation model representing a single chat session between user and AI."""
    id: UUID = Field(default_factory=uuid4, primary_key=True, description="Unique identifier for the conversation")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when conversation was initiated")
    updated_at: datetime = Field(default_factory=datetime.now, description="Timestamp of last activity in conversation")

    # Add indexes for better performance
    __table_args__ = (
        {'extend_existing': True}
    )

    # Relationship to messages - using string reference to avoid circular import
    messages: list["Message"] = Relationship(back_populates="conversation", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""
    pass


class ConversationRead(ConversationBase):
    """Schema for reading conversation data."""
    id: UUID
    created_at: datetime
    updated_at: datetime