"""Tests for JWT authentication and user isolation."""

import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import patch, MagicMock
import sys
import os

# Add the backend/src directory to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app  # Import your FastAPI app
from database.config import engine
from sqlmodel import Session, select
from src.models.user import User
from src.models.task import Task
from src.models.conversation import Conversation
from src.models.message import Message
from src.services.conversation_service import ConversationService
from src.services.message_service import MessageService


def test_jwt_token_validation():
    """Test that JWT tokens are properly validated."""
    client = TestClient(app)

    # Test with no token
    headers_no_token = {"Content-Type": "application/json"}
    payload = {
        "message": "Test message",
        "conversation_id": None
    }

    response_no_token = client.post("/api/chat", headers=headers_no_token, json=payload)

    # Should return 401 for unauthorized access
    assert response_no_token.status_code == 401

    # Test with malformed token
    headers_malformed = {
        "Authorization": "Bearer invalid.token.format",
        "Content-Type": "application/json"
    }

    response_malformed = client.post("/api/chat", headers=headers_malformed, json=payload)

    # Should return 401 for invalid token
    assert response_malformed.status_code in [401, 403]


def test_user_isolation_conversation_access():
    """Test that users can only access their own conversations."""
    with Session(engine) as session:
        # Create two test users
        user1_id = "test_user_isolation_1"
        user2_id = "test_user_isolation_2"

        # Create conversations for each user
        conv_data_1 = Conversation(user_id=user1_id, title="User 1's conversation")
        conv_data_2 = Conversation(user_id=user2_id, title="User 2's conversation")

        session.add(conv_data_1)
        session.add(conv_data_2)
        session.commit()

        # Test the validation function directly
        user1_can_access_conv1 = MessageService.validate_user_access_to_conversation(
            session, conv_data_1.id, user1_id
        )
        user1_can_access_conv2 = MessageService.validate_user_access_to_conversation(
            session, conv_data_2.id, user1_id
        )
        user2_can_access_conv1 = MessageService.validate_user_access_to_conversation(
            session, conv_data_1.id, user2_id
        )
        user2_can_access_conv2 = MessageService.validate_user_access_to_conversation(
            session, conv_data_2.id, user2_id
        )

        # Verify isolation
        assert user1_can_access_conv1 is True  # User 1 can access their own conversation
        assert user1_can_access_conv2 is False  # User 1 cannot access User 2's conversation
        assert user2_can_access_conv1 is False  # User 2 cannot access User 1's conversation
        assert user2_can_access_conv2 is True  # User 2 can access their own conversation

        # Clean up
        session.delete(conv_data_1)
        session.delete(conv_data_2)
        session.commit()


def test_user_isolation_message_access():
    """Test that users can only access their own messages."""
    with Session(engine) as session:
        # Create two test users
        user1_id = "test_user_msg_isolation_1"
        user2_id = "test_user_msg_isolation_2"

        # Create a conversation for user 1
        conv_data = Conversation(user_id=user1_id, title="Shared conversation test")
        session.add(conv_data)
        session.commit()
        conv_id = conv_data.id

        # Create messages for each user in the same conversation
        from uuid import uuid4
        msg_data_1 = Message(
            user_id=user1_id,
            conversation_id=conv_id,
            role="user",
            content="User 1's message"
        )
        msg_data_2 = Message(
            user_id=user2_id,  # Different user in same conversation (hypothetical scenario)
            conversation_id=conv_id,
            role="user",
            content="User 2's message"
        )

        session.add(msg_data_1)
        session.add(msg_data_2)
        session.commit()

        # Test message access validation
        user1_can_access_msg1 = MessageService.validate_user_access_to_message(
            session, msg_data_1.id, user1_id
        )
        user1_can_access_msg2 = MessageService.validate_user_access_to_message(
            session, msg_data_2.id, user1_id
        )
        user2_can_access_msg1 = MessageService.validate_user_access_to_message(
            session, msg_data_1.id, user2_id
        )
        user2_can_access_msg2 = MessageService.validate_user_access_to_message(
            session, msg_data_2.id, user2_id
        )

        # Verify isolation
        assert user1_can_access_msg1 is True  # User 1 can access their own message
        assert user1_can_access_msg2 is False  # User 1 cannot access User 2's message
        assert user2_can_access_msg1 is False  # User 2 cannot access User 1's message
        assert user2_can_access_msg2 is True  # User 2 can access their own message

        # Clean up
        session.delete(msg_data_1)
        session.delete(msg_data_2)
        session.delete(conv_data)
        session.commit()


def test_conversation_listing_isolation():
    """Test that users only see their own conversations."""
    with Session(engine) as session:
        # Create test users
        user1_id = "test_user_conv_list_1"
        user2_id = "test_user_conv_list_2"

        # Create conversations for each user
        conv1_user1 = Conversation(user_id=user1_id, title="User 1 - Conv 1")
        conv2_user1 = Conversation(user_id=user1_id, title="User 1 - Conv 2")
        conv1_user2 = Conversation(user_id=user2_id, title="User 2 - Conv 1")
        conv2_user2 = Conversation(user_id=user2_id, title="User 2 - Conv 2")

        session.add_all([conv1_user1, conv2_user1, conv1_user2, conv2_user2])
        session.commit()

        # Get conversations for each user
        user1_convs = ConversationService.get_conversations_by_user(session, user1_id)
        user2_convs = ConversationService.get_conversations_by_user(session, user2_id)

        # Verify isolation
        assert len(user1_convs) >= 2  # At least the 2 we created
        assert len(user2_convs) >= 2  # At least the 2 we created

        # Verify user 1 only gets their own conversations
        for conv in user1_convs:
            assert conv.user_id == user1_id

        # Verify user 2 only gets their own conversations
        for conv in user2_convs:
            assert conv.user_id == user2_id

        # Clean up
        session.delete(conv1_user1)
        session.delete(conv2_user1)
        session.delete(conv1_user2)
        session.delete(conv2_user2)
        session.commit()


def test_message_listing_isolation():
    """Test that users only see their own messages."""
    with Session(engine) as session:
        # Create test users and conversation
        user1_id = "test_user_msg_list_1"
        user2_id = "test_user_msg_list_2"

        conv = Conversation(user_id=user1_id, title="Test conversation")
        session.add(conv)
        session.commit()
        conv_id = conv.id

        # Create messages for each user
        msg1_user1 = Message(
            user_id=user1_id,
            conversation_id=conv_id,
            role="user",
            content="User 1's message"
        )
        msg2_user1 = Message(
            user_id=user1_id,
            conversation_id=conv_id,
            role="assistant",
            content="Assistant response to User 1"
        )
        msg1_user2 = Message(
            user_id=user2_id,
            conversation_id=conv_id,  # Same conversation (hypothetical shared scenario)
            role="user",
            content="User 2's message"
        )

        session.add_all([msg1_user1, msg2_user1, msg1_user2])
        session.commit()

        # Get messages for each user
        user1_msgs = MessageService.get_messages_by_user(session, user1_id)
        user2_msgs = MessageService.get_messages_by_user(session, user2_id)

        # Verify isolation
        for msg in user1_msgs:
            assert msg.user_id == user1_id

        for msg in user2_msgs:
            assert msg.user_id == user2_id

        # Clean up
        session.delete(msg1_user1)
        session.delete(msg2_user1)
        session.delete(msg1_user2)
        session.delete(conv)
        session.commit()


def test_task_ownership_verification():
    """Test that tasks are properly isolated by user."""
    with Session(engine) as session:
        # Create test users
        user1_id = "test_user_task_owner_1"
        user2_id = "test_user_task_owner_2"

        # Create tasks for each user
        task1_user1 = Task(
            user_id=user1_id,
            title="User 1's task",
            description="Description for user 1's task",
            completed=False
        )
        task2_user1 = Task(
            user_id=user1_id,
            title="Another task for User 1",
            description="Another description",
            completed=True
        )
        task1_user2 = Task(
            user_id=user2_id,
            title="User 2's task",
            description="Description for user 2's task",
            completed=False
        )

        session.add_all([task1_user1, task2_user1, task1_user2])
        session.commit()

        # Verify that each user's tasks have correct ownership
        stmt_user1 = select(Task).where(Task.user_id == user1_id)
        user1_tasks = session.exec(stmt_user1).all()

        stmt_user2 = select(Task).where(Task.user_id == user2_id)
        user2_tasks = session.exec(stmt_user2).all()

        # Verify user 1 tasks
        assert len(user1_tasks) >= 2  # At least the 2 we created
        for task in user1_tasks:
            assert task.user_id == user1_id

        # Verify user 2 tasks
        assert len(user2_tasks) >= 1  # At least the 1 we created
        for task in user2_tasks:
            assert task.user_id == user2_id

        # Clean up
        session.delete(task1_user1)
        session.delete(task2_user1)
        session.delete(task1_user2)
        session.commit()


if __name__ == "__main__":
    test_jwt_token_validation()
    test_user_isolation_conversation_access()
    test_user_isolation_message_access()
    test_conversation_listing_isolation()
    test_message_listing_isolation()
    test_task_ownership_verification()
    print("All authentication and isolation tests passed!")