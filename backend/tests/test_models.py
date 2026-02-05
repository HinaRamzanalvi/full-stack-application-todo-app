"""Unit tests for Conversation and Message models."""

import pytest
from datetime import datetime
from uuid import UUID
from sqlmodel import Session, select
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.conversation import Conversation, ConversationCreate
from src.models.message import Message, MessageCreate, MessageRole
from database.config import engine


def test_conversation_model_creation():
    """Test creating a Conversation model instance."""
    user_id = "test_user_123"

    conversation_data = ConversationCreate(
        user_id=user_id,
        title="Test Conversation"
    )

    conversation = Conversation(
        user_id=conversation_data.user_id,
        title=conversation_data.title
    )

    assert conversation.user_id == user_id
    assert conversation.title == "Test Conversation"
    assert isinstance(conversation.id, UUID)
    assert isinstance(conversation.created_at, datetime)
    assert isinstance(conversation.updated_at, datetime)


def test_message_model_creation():
    """Test creating a Message model instance."""
    from uuid import uuid4

    user_id = "test_user_123"
    conversation_id = uuid4()

    message_data = MessageCreate(
        user_id=user_id,
        conversation_id=conversation_id,
        role=MessageRole.USER,
        content="Test message content"
    )

    message = Message(
        user_id=message_data.user_id,
        conversation_id=message_data.conversation_id,
        role=message_data.role,
        content=message_data.content
    )

    assert message.user_id == user_id
    assert message.conversation_id == conversation_id
    assert message.role == MessageRole.USER
    assert message.content == "Test message content"
    assert isinstance(message.id, UUID)
    assert isinstance(message.created_at, datetime)


def test_conversation_message_relationship():
    """Test the relationship between Conversation and Message models."""
    from uuid import uuid4

    # Create a conversation
    user_id = "test_user_123"
    conversation_data = ConversationCreate(user_id=user_id, title="Test Conversation")
    conversation = Conversation(
        user_id=conversation_data.user_id,
        title=conversation_data.title
    )

    # Create a message associated with the conversation
    message_data = MessageCreate(
        user_id=user_id,
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content="Test message"
    )
    message = Message(
        user_id=message_data.user_id,
        conversation_id=message_data.conversation_id,
        role=message_data.role,
        content=message_data.content
    )

    # The relationship should be accessible (though not loaded until queried)
    # This test mainly verifies the model structure is correct
    assert message.conversation_id == conversation.id
    assert message.user_id == user_id


def test_database_integration():
    """Test model creation with database integration."""
    # Create a new session for testing
    with Session(engine) as session:
        # Create a test conversation
        user_id = "test_user_db_123"
        conversation_data = ConversationCreate(
            user_id=user_id,
            title="Database Test Conversation"
        )

        conversation = Conversation(
            user_id=conversation_data.user_id,
            title=conversation_data.title,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        # Verify it was created with an ID
        assert conversation.id is not None
        assert conversation.user_id == user_id

        # Clean up - delete the test record
        session.delete(conversation)
        session.commit()


if __name__ == "__main__":
    test_conversation_model_creation()
    test_message_model_creation()
    test_conversation_message_relationship()
    print("All model tests passed!")