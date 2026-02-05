"""Unit tests for MCP tools."""

import pytest
from sqlmodel import Session
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tools.mcp_tools import (
    add_task_tool, list_tasks_tool, update_task_tool,
    complete_task_tool, delete_task_tool, execute_tool,
    TaskInput, TaskUpdateInput, TaskIdInput
)
from database.config import engine


def test_add_task_tool():
    """Test the add_task_tool function."""
    with Session(engine) as session:
        user_id = "test_user_add_task_123"

        # Create task input
        task_input = TaskInput(
            title="Test Task from Tool",
            description="Test description",
            user_id=user_id
        )

        # Execute the tool
        result = add_task_tool(session, task_input)

        # Verify success
        assert result["success"] is True
        assert "task_id" in result["result"]
        assert result["result"]["title"] == "Test Task from Tool"
        assert result["result"]["description"] == "Test description"
        assert result["result"]["completed"] is False

        # Clean up - delete the task
        task_id = result["result"]["task_id"]
        delete_input = TaskIdInput(task_id=task_id)
        delete_result = delete_task_tool(session, delete_input)
        assert delete_result["success"] is True


def test_list_tasks_tool():
    """Test the list_tasks_tool function."""
    with Session(engine) as session:
        user_id = "test_user_list_tasks_123"

        # First add a task to ensure there's something to list
        task_input = TaskInput(
            title="Task to List",
            description="Description for listing",
            user_id=user_id
        )
        add_result = add_task_tool(session, task_input)
        assert add_result["success"] is True
        task_id = add_result["result"]["task_id"]

        # Now list tasks for this user
        result = list_tasks_tool(session, user_id)

        # Verify success and that our task is in the list
        assert result["success"] is True
        assert "tasks" in result["result"]
        tasks = result["result"]["tasks"]

        # Find our task in the list
        our_task = None
        for task in tasks:
            if task["task_id"] == task_id:
                our_task = task
                break

        assert our_task is not None
        assert our_task["title"] == "Task to List"
        assert our_task["description"] == "Description for listing"
        assert our_task["completed"] is False

        # Clean up - delete the task
        delete_input = TaskIdInput(task_id=task_id)
        delete_result = delete_task_tool(session, delete_input)
        assert delete_result["success"] is True


def test_update_task_tool():
    """Test the update_task_tool function."""
    with Session(engine) as session:
        user_id = "test_user_update_task_123"

        # First add a task to update
        task_input = TaskInput(
            title="Original Task Title",
            description="Original description",
            user_id=user_id
        )
        add_result = add_task_tool(session, task_input)
        assert add_result["success"] is True
        task_id = add_result["result"]["task_id"]

        # Update the task
        task_update_input = TaskUpdateInput(
            task_id=task_id,
            title="Updated Task Title",
            description="Updated description",
            completed=True
        )

        result = update_task_tool(session, task_update_input)

        # Verify success and update
        assert result["success"] is True
        assert result["result"]["title"] == "Updated Task Title"
        assert result["result"]["description"] == "Updated description"
        assert result["result"]["completed"] is True

        # Clean up - delete the task
        delete_input = TaskIdInput(task_id=task_id)
        delete_result = delete_task_tool(session, delete_input)
        assert delete_result["success"] is True


def test_complete_task_tool():
    """Test the complete_task_tool function."""
    with Session(engine) as session:
        user_id = "test_user_complete_task_123"

        # First add a task to complete
        task_input = TaskInput(
            title="Task to Complete",
            description="Description for completion",
            user_id=user_id
        )
        add_result = add_task_tool(session, task_input)
        assert add_result["success"] is True
        task_id = add_result["result"]["task_id"]

        # Verify task is initially not completed
        list_result = list_tasks_tool(session, user_id)
        tasks = list_result["result"]["tasks"]
        original_task = next((t for t in tasks if t["task_id"] == task_id), None)
        assert original_task is not None
        assert original_task["completed"] is False

        # Complete the task
        task_input_complete = TaskIdInput(task_id=task_id)
        result = complete_task_tool(session, task_input_complete)

        # Verify success and completion
        assert result["success"] is True
        assert result["result"]["task_id"] == task_id
        assert result["result"]["completed"] is True

        # Verify completion in database
        list_result_after = list_tasks_tool(session, user_id)
        tasks_after = list_result_after["result"]["tasks"]
        completed_task = next((t for t in tasks_after if t["task_id"] == task_id), None)
        assert completed_task is not None
        assert completed_task["completed"] is True

        # Clean up - delete the task
        delete_result = delete_task_tool(session, task_input_complete)
        assert delete_result["success"] is True


def test_delete_task_tool():
    """Test the delete_task_tool function."""
    with Session(engine) as session:
        user_id = "test_user_delete_task_123"

        # First add a task to delete
        task_input = TaskInput(
            title="Task to Delete",
            description="Description for deletion",
            user_id=user_id
        )
        add_result = add_task_tool(session, task_input)
        assert add_result["success"] is True
        task_id = add_result["result"]["task_id"]

        # Verify task exists before deletion
        list_result_before = list_tasks_tool(session, user_id)
        tasks_before = [t for t in list_result_before["result"]["tasks"] if t["task_id"] == task_id]
        assert len(tasks_before) == 1

        # Delete the task
        task_input_delete = TaskIdInput(task_id=task_id)
        result = delete_task_tool(session, task_input_delete)

        # Verify success and deletion
        assert result["success"] is True
        assert result["result"]["task_id"] == task_id

        # Verify task no longer exists
        list_result_after = list_tasks_tool(session, user_id)
        tasks_after = [t for t in list_result_after["result"]["tasks"] if t["task_id"] == task_id]
        assert len(tasks_after) == 0


def test_execute_tool_function():
    """Test the execute_tool function wrapper."""
    with Session(engine) as session:
        user_id = "test_user_execute_tool_123"

        # Test executing add_task tool through execute_tool
        result = execute_tool(
            "add_task",
            session,
            title="Executed Task",
            description="Task added via execute_tool",
            user_id=user_id
        )

        assert result["success"] is True
        assert "task_id" in result["result"]
        task_id = result["result"]["task_id"]

        # Test executing list_tasks tool through execute_tool
        list_result = execute_tool("list_tasks", session, user_id=user_id)
        assert list_result["success"] is True
        tasks = list_result["result"]["tasks"]
        task_found = any(t["task_id"] == task_id for t in tasks)
        assert task_found is True

        # Clean up - delete the task
        delete_result = execute_tool("delete_task", session, task_id=task_id)
        assert delete_result["success"] is True


def test_execute_tool_invalid():
    """Test executing an invalid tool."""
    with Session(engine) as session:
        result = execute_tool("invalid_tool", session)
        assert result["success"] is False
        assert "Unknown tool: invalid_tool" in result["error"]


if __name__ == "__main__":
    test_add_task_tool()
    test_list_tasks_tool()
    test_update_task_tool()
    test_complete_task_tool()
    test_delete_task_tool()
    test_execute_tool_function()
    test_execute_tool_invalid()
    print("All MCP tools tests passed!")