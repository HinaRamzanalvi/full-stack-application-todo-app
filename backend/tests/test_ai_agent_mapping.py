"""Tests for AI agent response mapping to MCP tool actions."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import sys
import os

# Add the backend/src directory to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.services.ai_agent_service import AIAgentService
from src.tools.mcp_tools import execute_tool
from sqlmodel import Session


def test_process_with_rules_add_task():
    """Test rule-based processing for add_task commands."""
    with patch('src.tools.mcp_tools.execute_tool') as mock_execute_tool:
        # Mock the tool execution to return a success result
        mock_execute_tool.return_value = {
            "success": True,
            "result": {
                "task_id": "test-task-id-123",
                "title": "Buy groceries",
                "description": None,
                "completed": False
            },
            "message": "Task 'Buy groceries' added successfully"
        }

        # Create an instance of the AI agent service
        ai_agent = AIAgentService()

        # Mock the database session
        mock_session = MagicMock(spec=Session)

        # Call the rule-based processor with an add task command
        result = ai_agent._process_with_rules(
            mock_session,
            "test_user_123",
            "Add task: Buy groceries"
        )

        # Verify the result structure
        assert result["response"] == "Task 'Buy groceries' added successfully"
        assert result["action_result"]["type"] == "add_task"
        assert result["action_result"]["success"] is True

        # Verify the tool was called with correct parameters
        mock_execute_tool.assert_called_once()
        args, kwargs = mock_execute_tool.call_args
        assert args[0] == "add_task"
        assert kwargs["title"] == "Buy groceries"
        assert kwargs["user_id"] == "test_user_123"


def test_process_with_rules_list_tasks():
    """Test rule-based processing for list_tasks commands."""
    with patch('src.tools.mcp_tools.execute_tool') as mock_execute_tool:
        # Mock the tool execution to return a list of tasks
        mock_execute_tool.return_value = {
            "success": True,
            "result": {
                "tasks": [
                    {
                        "task_id": "task-1",
                        "title": "Buy groceries",
                        "description": "Milk, bread, eggs",
                        "completed": False,
                        "created_at": "2026-01-31T10:00:00"
                    },
                    {
                        "task_id": "task-2",
                        "title": "Walk the dog",
                        "description": "Evening walk around the block",
                        "completed": True,
                        "created_at": "2026-01-31T09:00:00"
                    }
                ]
            },
            "message": "Found 2 tasks for user"
        }

        ai_agent = AIAgentService()
        mock_session = MagicMock(spec=Session)

        result = ai_agent._process_with_rules(
            mock_session,
            "test_user_123",
            "Show my tasks"
        )

        assert result["action_result"]["type"] == "list_tasks"
        assert result["action_result"]["success"] is True
        assert "2 tasks" in result["response"]

        # Verify the tool was called correctly
        mock_execute_tool.assert_called_once_with("list_tasks", mock_session, user_id="test_user_123")


def test_process_with_rules_complete_task():
    """Test rule-based processing for complete_task commands."""
    with patch('src.tools.mcp_tools.execute_tool') as mock_execute_tool:
        # First call (list_tasks) to find the task
        list_mock_result = {
            "success": True,
            "result": {
                "tasks": [
                    {
                        "task_id": "task-to-complete-123",
                        "title": "Buy groceries",
                        "description": "Milk, bread, eggs",
                        "completed": False
                    }
                ]
            },
            "message": "Found 1 task for user"
        }

        # Second call (complete_task) to complete the task
        complete_mock_result = {
            "success": True,
            "result": {
                "task_id": "task-to-complete-123",
                "completed": True
            },
            "message": "Task 'Buy groceries' marked as completed"
        }

        # Configure the mock to return different results on subsequent calls
        mock_execute_tool.side_effect = [list_mock_result, complete_mock_result]

        ai_agent = AIAgentService()
        mock_session = MagicMock(spec=Session)

        result = ai_agent._process_with_rules(
            mock_session,
            "test_user_123",
            "Complete task: Buy groceries"
        )

        assert result["action_result"]["type"] == "complete_task"
        assert result["action_result"]["success"] is True
        assert "marked as completed" in result["response"]

        # Verify both tools were called
        assert mock_execute_tool.call_count == 2
        first_call, second_call = mock_execute_tool.call_args_list
        assert first_call[0][0] == "list_tasks"  # First call is list_tasks
        assert second_call[0][0] == "complete_task"  # Second call is complete_task


def test_process_with_rules_delete_task():
    """Test rule-based processing for delete_task commands."""
    with patch('src.tools.mcp_tools.execute_tool') as mock_execute_tool:
        # First call (list_tasks) to find the task
        list_mock_result = {
            "success": True,
            "result": {
                "tasks": [
                    {
                        "task_id": "task-to-delete-123",
                        "title": "Old task to remove",
                        "description": "No longer needed",
                        "completed": False
                    }
                ]
            },
            "message": "Found 1 task for user"
        }

        # Second call (delete_task) to delete the task
        delete_mock_result = {
            "success": True,
            "result": {
                "task_id": "task-to-delete-123",
                "message": "Task 'Old task to remove' deleted successfully"
            },
            "message": "Task 'Old task to remove' deleted successfully"
        }

        mock_execute_tool.side_effect = [list_mock_result, delete_mock_result]

        ai_agent = AIAgentService()
        mock_session = MagicMock(spec=Session)

        result = ai_agent._process_with_rules(
            mock_session,
            "test_user_123",
            "Delete task: Old task to remove"
        )

        assert result["action_result"]["type"] == "delete_task"
        assert result["action_result"]["success"] is True
        assert "deleted successfully" in result["response"]

        # Verify both tools were called
        assert mock_execute_tool.call_count == 2


def test_process_with_rules_unknown_command():
    """Test rule-based processing for unknown commands."""
    ai_agent = AIAgentService()
    mock_session = MagicMock(spec=Session)

    result = ai_agent._process_with_rules(
        mock_session,
        "test_user_123",
        "This is an unknown command that should trigger default response"
    )

    assert result["action_result"]["type"] == "unknown_command"
    assert result["action_result"]["success"] is False
    assert "I understood your message" in result["response"]
    assert "I can help you manage tasks" in result["response"]


def test_process_with_rules_update_task():
    """Test rule-based processing for update_task commands."""
    with patch('src.tools.mcp_tools.execute_tool') as mock_execute_tool:
        # First call (list_tasks) to find the task
        list_mock_result = {
            "success": True,
            "result": {
                "tasks": [
                    {
                        "task_id": "task-to-update-123",
                        "title": "Old task title",
                        "description": "Original description",
                        "completed": False
                    }
                ]
            },
            "message": "Found 1 task for user"
        }

        # Second call (update_task) to update the task
        update_mock_result = {
            "success": True,
            "result": {
                "task_id": "task-to-update-123",
                "title": "New task title",
                "description": "Original description",
                "completed": False
            },
            "message": "I've updated the task 'Old task title' to 'New task title'."
        }

        mock_execute_tool.side_effect = [list_mock_result, update_mock_result]

        ai_agent = AIAgentService()
        mock_session = MagicMock(spec=Session)

        result = ai_agent._process_with_rules(
            mock_session,
            "test_user_123",
            'Update task "Old task title" to "New task title"'
        )

        assert result["action_result"]["type"] == "update_task"
        assert result["action_result"]["success"] is True
        assert "updated the task" in result["response"]

        # Verify both tools were called
        assert mock_execute_tool.call_count == 2


def test_process_with_rules_error_handling():
    """Test error handling in rule-based processing."""
    with patch('src.tools.mcp_tools.execute_tool') as mock_execute_tool:
        # Mock an error in the tool execution
        mock_execute_tool.return_value = {
            "success": False,
            "error": "Task not found",
            "message": "Task not found or you don't have permission to update this task"
        }

        ai_agent = AIAgentService()
        mock_session = MagicMock(spec=Session)

        result = ai_agent._process_with_rules(
            mock_session,
            "test_user_123",
            "Update task: Non-existent task"
        )

        # Even with an error, it should still return the right action type
        assert result["action_result"]["type"] == "update_task"
        assert result["action_result"]["success"] is False
        # The response should reflect the error
        assert "couldn't find" in result["response"] or "not found" in result["response"]


def test_tool_execution_mapping():
    """Test that the execute_tool function correctly maps to different tools."""
    with patch('src.models.task.Task') as mock_task_model:
        from tools.mcp_tools import (
            add_task_tool, list_tasks_tool, update_task_tool,
            complete_task_tool, delete_task_tool, execute_tool,
            TaskInput, TaskUpdateInput, TaskIdInput
        )

        mock_session = MagicMock(spec=Session)

        # Test add_task execution
        task_input = TaskInput(
            title="Test task for mapping",
            description="Testing tool mapping",
            user_id="test_user_mapping_123"
        )
        add_result = add_task_tool(mock_session, task_input)

        # Verify it returns the right structure
        assert "success" in add_result
        assert "result" in add_result

        # Test execute_tool function with add_task
        exec_result = execute_tool("add_task", mock_session,
                                  title="Exec test task",
                                  description="Testing execute function",
                                  user_id="test_user_exec_123")

        assert "success" in exec_result
        assert exec_result["success"] is False  # Will fail without real DB setup, but function should execute


def test_response_structure_consistency():
    """Test that all AI responses follow the same structure."""
    ai_agent = AIAgentService()

    # Test the structure of the response regardless of content
    mock_session = MagicMock(spec=Session)

    # Test with a simple command
    result = ai_agent._process_with_rules(
        mock_session,
        "test_user_123",
        "Just a simple message"
    )

    # Verify consistent response structure
    assert isinstance(result, dict)
    assert "response" in result
    assert "action_result" in result

    action_result = result["action_result"]
    assert isinstance(action_result, dict)
    assert "type" in action_result
    assert "success" in action_result
    assert "result" in action_result


if __name__ == "__main__":
    test_process_with_rules_add_task()
    test_process_with_rules_list_tasks()
    test_process_with_rules_complete_task()
    test_process_with_rules_delete_task()
    test_process_with_rules_unknown_command()
    test_process_with_rules_update_task()
    test_process_with_rules_error_handling()
    test_tool_execution_mapping()
    test_response_structure_consistency()
    print("All AI agent mapping tests passed!")