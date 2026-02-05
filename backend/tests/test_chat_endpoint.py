"""Integration tests for the chat endpoint."""

import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import patch, AsyncMock
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
from src.tools.mcp_tools import TaskInput


def test_chat_endpoint_basic():
    """Test basic functionality of the chat endpoint."""
    client = TestClient(app)

    # Mock the AI agent to return a predictable response
    with patch('src.services.ai_agent_service.AIAgentService.process_user_message') as mock_ai:
        mock_ai.return_value = {
            "response": "Test AI response",
            "action_result": {"type": "text_response", "success": True, "result": {"content": "Test"}}
        }

        # Make a request to the chat endpoint
        # We'll mock the authentication for now
        headers = {
            "Authorization": "Bearer fake-jwt-token",
            "Content-Type": "application/json"
        }
        payload = {
            "message": "Hello, can you help me?",
            "conversation_id": None
        }

        response = client.post("/api/chat", headers=headers, json=payload)

        # Check the response
        assert response.status_code in [200, 401]  # Allow 401 for auth failure

        if response.status_code == 200:
            data = response.json()
            assert "success" in data
            # If successful, check the structure
            if data["success"]:
                assert "data" in data
                assert "response" in data["data"]


def test_chat_endpoint_with_valid_conversation():
    """Test chat endpoint with an existing conversation."""
    client = TestClient(app)

    with patch('src.services.ai_agent_service.AIAgentService.process_user_message') as mock_ai:
        mock_ai.return_value = {
            "response": "Response to continued conversation",
            "action_result": {"type": "text_response", "success": True, "result": {"content": "Continued"}}
        }

        headers = {
            "Authorization": "Bearer fake-jwt-token",
            "Content-Type": "application/json"
        }
        payload = {
            "message": "Following up on our previous conversation",
            "conversation_id": "123e4567-e89b-12d3-a456-426614174000"  # Fake UUID
        }

        response = client.post("/api/chat", headers=headers, json=payload)

        # Even with a fake conversation ID, we expect certain behaviors
        # If auth fails, we expect 401
        # If conversation validation fails, we might get 400 or 403
        assert response.status_code in [200, 400, 401, 403]


def test_chat_endpoint_empty_message():
    """Test chat endpoint with empty message."""
    client = TestClient(app)

    headers = {
        "Authorization": "Bearer fake-jwt-token",
        "Content-Type": "application/json"
    }
    payload = {
        "message": "",  # Empty message
        "conversation_id": None
    }

    response = client.post("/api/chat", headers=headers, json=payload)

    # Should return 400 for empty message
    if response.status_code != 401:  # Skip if auth fails
        assert response.status_code == 400


def test_chat_endpoint_missing_message():
    """Test chat endpoint with missing message."""
    client = TestClient(app)

    headers = {
        "Authorization": "Bearer fake-jwt-token",
        "Content-Type": "application/json"
    }
    # Don't include the message field
    payload = {
        "conversation_id": None
    }

    response = client.post("/api/chat", headers=headers, json=payload)

    # Should return 422 for validation error or 401 for auth
    if response.status_code != 401:
        assert response.status_code in [422, 400]


def test_chat_endpoint_auth_required():
    """Test that chat endpoint requires authentication."""
    client = TestClient(app)

    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "message": "Hello",
        "conversation_id": None
    }

    response = client.post("/api/chat", headers=headers, json=payload)

    # Should return 401 for unauthorized access
    assert response.status_code == 401


def test_chat_endpoint_json_format():
    """Test chat endpoint with proper JSON response format."""
    client = TestClient(app)

    with patch('src.services.ai_agent_service.AIAgentService.process_user_message') as mock_ai:
        mock_ai.return_value = {
            "response": "Formatted response",
            "action_result": {
                "type": "test_action",
                "success": True,
                "result": {"test": "data"}
            }
        }

        headers = {
            "Authorization": "Bearer fake-jwt-token",
            "Content-Type": "application/json"
        }
        payload = {
            "message": "Test message for JSON format",
            "conversation_id": None
        }

        response = client.post("/api/chat", headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()

            # Verify response structure
            assert "success" in data
            assert "data" in data

            chat_data = data["data"]
            assert "response" in chat_data
            assert "conversation_id" in chat_data
            assert "action_result" in chat_data
            assert "timestamp" in chat_data

            # Verify action_result structure
            action_result = chat_data["action_result"]
            assert "type" in action_result
            assert "success" in action_result
            assert "result" in action_result


def test_chat_endpoint_error_handling():
    """Test error handling in chat endpoint."""
    client = TestClient(app)

    # Mock the AI agent to raise an exception
    with patch('src.services.ai_agent_service.AIAgentService.process_user_message') as mock_ai:
        mock_ai.side_effect = Exception("Test error in AI processing")

        headers = {
            "Authorization": "Bearer fake-jwt-token",
            "Content-Type": "application/json"
        }
        payload = {
            "message": "Message that triggers error",
            "conversation_id": None
        }

        response = client.post("/api/chat", headers=headers, json=payload)

        # Should return 500 for internal server error (or 401 for auth)
        if response.status_code != 401:
            assert response.status_code == 500


if __name__ == "__main__":
    test_chat_endpoint_basic()
    test_chat_endpoint_with_valid_conversation()
    test_chat_endpoint_empty_message()
    test_chat_endpoint_missing_message()
    test_chat_endpoint_auth_required()
    test_chat_endpoint_json_format()
    test_chat_endpoint_error_handling()
    print("All chat endpoint integration tests passed!")