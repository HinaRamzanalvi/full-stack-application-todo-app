"""Message model for chatbot functionality."""

from datetime import datetime
from enum import Enum
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from .conversation import Conversation


class MessageRole(str, Enum):
    """Enumeration for message roles."""
    USER = "user"
    ASSISTANT = "assistant"


class MessageBase(SQLModel):
    """Base class for Message model with common fields."""
    user_id: str = Field(index=True, nullable=False, description="ID of the user who sent this message")
    conversation_id: UUID = Field(index=True, nullable=False, foreign_key="conversation.id", description="ID of the conversation this message belongs to")
    role: MessageRole = Field(nullable=False, description="Identifies if message is from user or AI")
    content: str = Field(sa_column_kwargs={"nullable": False}, description="The actual message content")


class Message(MessageBase, table=True):
    """Message model representing an individual message in a conversation."""
    id: UUID = Field(default_factory=uuid4, primary_key=True, description="Unique identifier for the message")
    created_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"index": True}, description="Timestamp when message was created")

    # Add indexes for better performance
    __table_args__ = (
        {"extend_existing": True}
    )

    # Relationship to conversation - using string reference to avoid circular import
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    pass


class MessageRead(MessageBase):
    """Schema for reading message data."""
    id: UUID
    created_at: datetime