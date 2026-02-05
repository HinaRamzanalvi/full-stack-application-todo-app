"""Service for managing messages."""

from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from uuid import UUID
from ..models.message import Message, MessageCreate, MessageRole
from ..models.conversation import Conversation


class MessageService:
    """Service class for handling message operations."""

    @staticmethod
    def create_message(session: Session, message_data: MessageCreate) -> Message:
        """Create a new message."""
        message = Message(
            user_id=message_data.user_id,
            conversation_id=message_data.conversation_id,
            role=message_data.role,
            content=message_data.content,
            created_at=datetime.now()
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    def get_message_by_id(session: Session, message_id: UUID) -> Optional[Message]:
        """Retrieve a message by its ID."""
        statement = select(Message).where(Message.id == message_id)
        return session.exec(statement).first()

    @staticmethod
    def get_messages_by_conversation(session: Session, conversation_id: UUID) -> List[Message]:
        """Retrieve all messages for a specific conversation."""
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.asc())
        return session.exec(statement).all()

    @staticmethod
    def get_messages_by_user(session: Session, user_id: str) -> List[Message]:
        """Retrieve all messages for a specific user."""
        statement = select(Message).where(Message.user_id == user_id).order_by(Message.created_at.desc())
        return session.exec(statement).all()

    @staticmethod
    def get_latest_messages_for_user(session: Session, user_id: str, limit: int = 10) -> List[Message]:
        """Retrieve the latest messages for a specific user."""
        statement = select(Message).where(Message.user_id == user_id).order_by(Message.created_at.desc()).limit(limit)
        return session.exec(statement).all()

    @staticmethod
    def update_message_content(session: Session, message_id: UUID, content: str) -> Optional[Message]:
        """Update the content of a message."""
        message = MessageService.get_message_by_id(session, message_id)
        if message:
            message.content = content
            session.add(message)
            session.commit()
            session.refresh(message)
        return message

    @staticmethod
    def delete_message(session: Session, message_id: UUID) -> bool:
        """Delete a message by its ID."""
        message = MessageService.get_message_by_id(session, message_id)
        if message:
            session.delete(message)
            session.commit()
            return True
        return False

    @staticmethod
    def validate_user_access_to_message(session: Session, message_id: UUID, user_id: str) -> bool:
        """Validate that a user has access to a specific message."""
        message = MessageService.get_message_by_id(session, message_id)
        return message and message.user_id == user_id

    @staticmethod
    def validate_user_access_to_conversation(session: Session, conversation_id: UUID, user_id: str) -> bool:
        """Validate that a user has access to a specific conversation."""
        statement = select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user_id)
        conversation = session.exec(statement).first()
        return conversation is not None