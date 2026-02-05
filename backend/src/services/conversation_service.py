"""Service for managing conversations."""

from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from uuid import UUID
from ..models.conversation import Conversation, ConversationCreate


class ConversationService:
    """Service class for handling conversation operations."""

    @staticmethod
    def create_conversation(session: Session, conversation_data: ConversationCreate) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            user_id=conversation_data.user_id,
            title=conversation_data.title,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: UUID) -> Optional[Conversation]:
        """Retrieve a conversation by its ID."""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return session.exec(statement).first()

    @staticmethod
    def get_conversations_by_user(session: Session, user_id: str) -> List[Conversation]:
        """Retrieve all conversations for a specific user."""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return session.exec(statement).all()

    @staticmethod
    def update_conversation_title(session: Session, conversation_id: UUID, title: str) -> Optional[Conversation]:
        """Update the title of a conversation."""
        conversation = ConversationService.get_conversation_by_id(session, conversation_id)
        if conversation:
            conversation.title = title
            conversation.updated_at = datetime.now()
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        return conversation

    @staticmethod
    def update_conversation_timestamp(session: Session, conversation_id: UUID) -> Optional[Conversation]:
        """Update the timestamp of a conversation to mark activity."""
        conversation = ConversationService.get_conversation_by_id(session, conversation_id)
        if conversation:
            conversation.updated_at = datetime.now()
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        return conversation

    @staticmethod
    def delete_conversation(session: Session, conversation_id: UUID) -> bool:
        """Delete a conversation by its ID."""
        conversation = ConversationService.get_conversation_by_id(session, conversation_id)
        if conversation:
            session.delete(conversation)
            session.commit()
            return True
        return False