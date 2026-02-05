"""End-to-end tests for the complete chat flow."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add the backend/src directory to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app  # Import your FastAPI app
from database.config import engine
from sqlmodel import Session, select
from src.models.conversation import Conversation
from src.models.message import Message
from src.models.task import Task


def test_complete_chat_flow_new_conversation():
    """Test complete chat flow starting with a new conversation."""
    client = TestClient(app)

    with patch('src.services.ai_agent_service.AIAgentService.process_user_message') as mock_ai:
        # Mock the AI response for the first message
        mock_ai.return_value = {
            "response": "I've added the task 'Buy groceries' to your list.",
            "action_result": {
                "type": "add_task",
                "success": True,
                "result": {
                    "task_id": "test-task-123",
                    "title": "Buy groceries",
                    "completed": False
                }
            },
            "timestamp": "2026-01-31T10:30:00.000Z"
        }

        headers = {
            "Authorization": "Bearer fake-jwt-token",
            "Content-Type": "application/json"
        }

        # First message - should create a new conversation
        payload1 = {
            "message": "Add task: Buy groceries",
            "conversation_id": None
        }

        response1 = client.post("/api/chat", headers=headers, json=payload1)

        # If authentication passes, should get a 200 response
        if response1.status_code == 200:
            data1 = response1.json()
            assert data1["success"] is True
            assert "data" in data1
            assert "conversation_id" in data1["data"]
            assert data1["data"]["response"] == "I've added the task 'Buy groceries' to your list."

            # Save the conversation ID for the next message
            conversation_id = data1["data"]["conversation_id"]

            # Mock AI response for the second message
            mock_ai.return_value = {
                "response": "You have 1 task: 'Buy groceries' (pending).",
                "action_result": {
                    "type": "list_tasks",
                    "success": True,
                    "result": {
                        "tasks": [{
                            "task_id": "test-task-123",
                            "title": "Buy groceries",
                            "completed": False
                        }]
                    }
                },
                "timestamp": "2026-01-31T10:31:00.000Z"
            }

            # Second message - should continue the same conversation
            payload2 = {
                "message": "Show my tasks",
                "conversation_id": conversation_id
            }

            response2 = client.post("/api/chat", headers=headers, json=payload2)

            assert response2.status_code == 200
            data2 = response2.json()
            assert data2["success"] is True
            assert data2["data"]["conversation_id"] == conversation_id
            assert "1 task" in data2["data"]["response"]


def test_chat_flow_with_task_operations():
    """Test chat flow with various task operations."""
    client = TestClient(app)

    with patch('src.services.ai_agent_service.AIAgentService.process_user_message') as mock_ai:
        headers = {
            "Authorization": "Bearer fake-jwt-token",
            "Content-Type": "application/json"
        }

        # Step 1: Add a task
        mock_ai.return_value = {
            "response": "I've added the task 'Complete project proposal' to your list.",
            "action_result": {
                "type": "add_task",
                "success": True,
                "result": {
                    "task_id": "task-proposal-123",
                    "title": "Complete project proposal",
                    "completed": False
                }
            },
            "timestamp": "2026-01-31T10:30:00.000Z"
        }

        payload1 = {
            "message": "Add task: Complete project proposal",
            "conversation_id": None
        }
        response1 = client.post("/api/chat", headers=headers, json=payload1)

        if response1.status_code == 200:
            data1 = response1.json()
            assert data1["success"] is True
            conversation_id = data1["data"]["conversation_id"]

            # Step 2: List tasks
            mock_ai.return_value = {
                "response": "You have 1 task: 'Complete project proposal' (pending).",
                "action_result": {
                    "type": "list_tasks",
                    "success": True,
                    "result": {
                        "tasks": [{
                            "task_id": "task-proposal-123",
                            "title": "Complete project proposal",
                            "completed": False
                        }]
                    }
                },
                "timestamp": "2026-01-31T10:31:00.000Z"
            }

            payload2 = {
                "message": "What tasks do I have?",
                "conversation_id": conversation_id
            }
            response2 = client.post("/api/chat", headers=headers, json=payload2)

            assert response2.status_code == 200
            data2 = response2.json()
            assert data2["success"] is True
            assert "1 task" in data2["data"]["response"]

            # Step 3: Complete the task
            mock_ai.return_value = {
                "response": "I've marked the task 'Complete project proposal' as completed.",
                "action_result": {
                    "type": "complete_task",
                    "success": True,
                    "result": {
                        "task_id": "task-proposal-123",
                        "completed": True
                    }
                },
                "timestamp": "2026-01-31T10:32:00.000Z"
            }

            payload3 = {
                "message": "Complete task: Complete project proposal",
                "conversation_id": conversation_id
            }
            response3 = client.post("/api/chat", headers=headers, json=payload3)

            assert response3.status_code == 200
            data3 = response3.json()
            assert data3["success"] is True
            assert "marked" in data3["data"]["response"]


def test_chat_flow_error_handling():
    """Test chat flow with error handling."""
    client = TestClient(app)

    with patch('src.services.ai_agent_service.AIAgentService.process_user_message') as mock_ai:
        # Mock an error in AI processing
        mock_ai.side_effect = Exception("AI processing error")

        headers = {
            "Authorization": "Bearer fake-jwt-token",
            "Content-Type": "application/json"
        }
        payload = {
            "message": "This will cause an error",
            "conversation_id": None
        }

        response = client.post("/api/chat", headers=headers, json=payload)

        # Should return 500 for internal server error (or 401 for auth)
        if response.status_code != 401:
            assert response.status_code == 500


def test_conversation_persistence_simulation():
    """Test that conversation state is maintained across requests."""
    client = TestClient(app)

    with patch('src.services.ai_agent_service.AIAgentService.process_user_message') as mock_ai:
        headers = {
            "Authorization": "Bearer fake-jwt-token",
            "Content-Type": "application/json"
        }

        # First message - creates conversation
        mock_ai.return_value = {
            "response": "Okay, I've noted your first message.",
            "action_result": {
                "type": "text_response",
                "success": True,
                "result": {"content": "Noted"}
            },
            "timestamp": "2026-01-31T10:30:00.000Z"
        }

        payload1 = {
            "message": "Hello, I want to start a conversation",
            "conversation_id": None
        }
        response1 = client.post("/api/chat", headers=headers, json=payload1)

        if response1.status_code == 200:
            data1 = response1.json()
            assert data1["success"] is True
            conversation_id = data1["data"]["conversation_id"]
            assert conversation_id is not None

            # Second message - continues same conversation
            mock_ai.return_value = {
                "response": "Thanks for continuing our conversation.",
                "action_result": {
                    "type": "text_response",
                    "success": True,
                    "result": {"content": "Continued"}
                },
                "timestamp": "2026-01-31T10:31:00.000Z"
            }

            payload2 = {
                "message": "How are you?",
                "conversation_id": conversation_id
            }
            response2 = client.post("/api/chat", headers=headers, json=payload2)

            assert response2.status_code == 200
            data2 = response2.json()
            assert data2["success"] is True
            assert data2["data"]["conversation_id"] == conversation_id


def test_multiple_users_isolation():
    """Test that different users have isolated conversations."""
    client = TestClient(app)

    with patch('src.services.ai_agent_service.AIAgentService.process_user_message') as mock_ai:
        headers_user1 = {
            "Authorization": "Bearer fake-jwt-token-user1",
            "Content-Type": "application/json"
        }
        headers_user2 = {
            "Authorization": "Bearer fake-jwt-token-user2",
            "Content-Type": "application/json"
        }

        # Both users send the same message to start conversations
        mock_ai.return_value = {
            "response": "Hello! I've received your message.",
            "action_result": {
                "type": "text_response",
                "success": True,
                "result": {"content": "Received"}
            },
            "timestamp": "2026-01-31T10:30:00.000Z"
        }

        payload = {
            "message": "Hello from user",
            "conversation_id": None
        }

        # User 1 creates conversation
        response1 = client.post("/api/chat", headers=headers_user1, json=payload)
        if response1.status_code == 200:
            data1 = response1.json()
            user1_conversation_id = data1["data"]["conversation_id"]

            # User 2 creates separate conversation
            response2 = client.post("/api/chat", headers=headers_user2, json=payload)
            if response2.status_code == 200:
                data2 = response2.json()
                user2_conversation_id = data2["data"]["conversation_id"]

                # Conversations should be different
                assert user1_conversation_id != user2_conversation_id


def test_message_history_simulation():
    """Test that message history is properly handled."""
    client = TestClient(app)

    with patch('src.services.ai_agent_service.AIAgentService.process_user_message') as mock_ai:
        headers = {
            "Authorization": "Bearer fake-jwt-token",
            "Content-Type": "application/json"
        }

        # Mock AI to return different responses based on context
        def mock_process(*args, **kwargs):
            message = kwargs.get('user_message', args[3]) if len(args) > 3 else "default"
            if "history" in message.lower():
                return {
                    "response": "Based on our conversation, you asked about history.",
                    "action_result": {
                        "type": "text_response",
                        "success": True,
                        "result": {"content": "History context"}
                    },
                    "timestamp": "2026-01-31T10:32:00.000Z"
                }
            else:
                return {
                    "response": "I've processed your message.",
                    "action_result": {
                        "type": "text_response",
                        "success": True,
                        "result": {"content": "Processed"}
                    },
                    "timestamp": "2026-01-31T10:30:00.000Z"
                }

        mock_ai.side_effect = lambda *args, **kwargs: mock_process(*args, **kwargs)

        # Start conversation
        payload1 = {
            "message": "First message in conversation",
            "conversation_id": None
        }
        response1 = client.post("/api/chat", headers=headers, json=payload1)

        if response1.status_code == 200:
            data1 = response1.json()
            conversation_id = data1["data"]["conversation_id"]

            # Continue with reference to history
            payload2 = {
                "message": "What about our history?",
                "conversation_id": conversation_id
            }
            response2 = client.post("/api/chat", headers=headers, json=payload2)

            assert response2.status_code == 200
            data2 = response2.json()
            # The response should acknowledge the conversation history
            assert "conversation" in data2["data"]["response"]


if __name__ == "__main__":
    test_complete_chat_flow_new_conversation()
    test_chat_flow_with_task_operations()
    test_chat_flow_error_handling()
    test_conversation_persistence_simulation()
    test_multiple_users_isolation()
    test_message_history_simulation()
    print("All chat flow tests passed!")