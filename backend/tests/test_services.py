"""Unit tests for Conversation and Message services."""

import pytest
from datetime import datetime
from uuid import uuid4
from sqlmodel import Session
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.conversation import ConversationCreate
from src.models.message import MessageCreate, MessageRole
from src.services.conversation_service import ConversationService
from src.services.message_service import MessageService
from database.config import engine


def test_conversation_service_create_and_get():
    """Test creating and retrieving a conversation."""
    with Session(engine) as session:
        user_id = "test_user_service_123"

        # Create conversation data
        conversation_data = ConversationCreate(
            user_id=user_id,
            title="Test Service Conversation"
        )

        # Create conversation using service
        created_conversation = ConversationService.create_conversation(session, conversation_data)

        # Verify creation
        assert created_conversation.id is not None
        assert created_conversation.user_id == user_id
        assert created_conversation.title == "Test Service Conversation"

        # Retrieve conversation using service
        retrieved_conversation = ConversationService.get_conversation_by_id(session, created_conversation.id)

        # Verify retrieval
        assert retrieved_conversation is not None
        assert retrieved_conversation.id == created_conversation.id
        assert retrieved_conversation.user_id == user_id

        # Clean up
        session.delete(created_conversation)
        session.commit()


def test_conversation_service_get_by_user():
    """Test retrieving conversations by user."""
    with Session(engine) as session:
        user_id = "test_user_multiple_123"

        # Create multiple conversations for the same user
        conv_data_1 = ConversationCreate(user_id=user_id, title="First Conversation")
        conv_data_2 = ConversationCreate(user_id=user_id, title="Second Conversation")

        conv1 = ConversationService.create_conversation(session, conv_data_1)
        conv2 = ConversationService.create_conversation(session, conv_data_2)

        # Get conversations by user
        user_conversations = ConversationService.get_conversations_by_user(session, user_id)

        # Verify we got both conversations
        assert len(user_conversations) >= 2  # May have more from other tests

        # Verify our conversations are in the list
        conv_ids = [conv.id for conv in user_conversations]
        assert conv1.id in conv_ids
        assert conv2.id in conv_ids

        # Clean up
        session.delete(conv1)
        session.delete(conv2)
        session.commit()


def test_message_service_create_and_get():
    """Test creating and retrieving a message."""
    with Session(engine) as session:
        user_id = "test_user_msg_service_123"

        # First create a conversation
        conv_data = ConversationCreate(user_id=user_id, title="Test Conversation for Messages")
        conversation = ConversationService.create_conversation(session, conv_data)

        # Create message data
        message_data = MessageCreate(
            user_id=user_id,
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content="Test message content"
        )

        # Create message using service
        created_message = MessageService.create_message(session, message_data)

        # Verify creation
        assert created_message.id is not None
        assert created_message.user_id == user_id
        assert created_message.conversation_id == conversation.id
        assert created_message.role == MessageRole.USER
        assert created_message.content == "Test message content"

        # Retrieve message using service
        retrieved_message = MessageService.get_message_by_id(session, created_message.id)

        # Verify retrieval
        assert retrieved_message is not None
        assert retrieved_message.id == created_message.id
        assert retrieved_message.content == "Test message content"

        # Clean up
        session.delete(created_message)
        session.delete(conversation)
        session.commit()


def test_message_service_get_by_conversation():
    """Test retrieving messages by conversation."""
    with Session(engine) as session:
        user_id = "test_user_msg_conv_123"

        # Create a conversation
        conv_data = ConversationCreate(user_id=user_id, title="Conversation with Multiple Messages")
        conversation = ConversationService.create_conversation(session, conv_data)

        # Create multiple messages in the same conversation
        msg_data_1 = MessageCreate(
            user_id=user_id,
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content="First message"
        )
        msg_data_2 = MessageCreate(
            user_id=user_id,
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content="Second message"
        )

        msg1 = MessageService.create_message(session, msg_data_1)
        msg2 = MessageService.create_message(session, msg_data_2)

        # Get messages by conversation
        conversation_messages = MessageService.get_messages_by_conversation(session, conversation.id)

        # Verify we got both messages
        assert len(conversation_messages) >= 2  # May have more from other tests

        # Verify our messages are in the list
        msg_ids = [msg.id for msg in conversation_messages]
        assert msg1.id in msg_ids
        assert msg2.id in msg_ids

        # Clean up
        session.delete(msg1)
        session.delete(msg2)
        session.delete(conversation)
        session.commit()


def test_user_access_validation():
    """Test user access validation for conversations and messages."""
    with Session(engine) as session:
        user1_id = "test_user_access_1"
        user2_id = "test_user_access_2"

        # Create conversations for different users
        conv_data_1 = ConversationCreate(user_id=user1_id, title="User 1's Conversation")
        conv_data_2 = ConversationCreate(user_id=user2_id, title="User 2's Conversation")

        conv1 = ConversationService.create_conversation(session, conv_data_1)
        conv2 = ConversationService.create_conversation(session, conv_data_2)

        # Test access validation
        # User 1 should have access to conversation 1 but not conversation 2
        assert MessageService.validate_user_access_to_conversation(session, conv1.id, user1_id) is True
        assert MessageService.validate_user_access_to_conversation(session, conv2.id, user1_id) is False

        # User 2 should have access to conversation 2 but not conversation 1
        assert MessageService.validate_user_access_to_conversation(session, conv2.id, user2_id) is True
        assert MessageService.validate_user_access_to_conversation(session, conv1.id, user2_id) is False

        # Clean up
        session.delete(conv1)
        session.delete(conv2)
        session.commit()


if __name__ == "__main__":
    test_conversation_service_create_and_get()
    test_conversation_service_get_by_user()
    test_message_service_create_and_get()
    test_message_service_get_by_conversation()
    test_user_access_validation()
    print("All service tests passed!")