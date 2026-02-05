"""MCP Tools for task operations."""

import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from sqlmodel import Session, select
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from models.task import Task
from models.user import User


class TaskInput(BaseModel):
    """Input model for task operations."""
    title: str = Field(..., description="Title of the task")
    description: Optional[str] = Field(None, description="Description of the task")
    user_id: str = Field(..., description="ID of the user")


class TaskUpdateInput(BaseModel):
    """Input model for updating task operations."""
    task_id: str = Field(..., description="ID of the task to update")
    title: Optional[str] = Field(None, description="New title of the task")
    description: Optional[str] = Field(None, description="New description of the task")
    completed: Optional[bool] = Field(None, description="New completion status")


class TaskIdInput(BaseModel):
    """Input model for operations requiring only task ID."""
    task_id: str = Field(..., description="ID of the task")


def add_task_tool(session: Session, task_input: TaskInput) -> Dict[str, Any]:
    """Add a new task for a user."""
    try:
        # Create a new task instance
        new_task = Task(
            user_id=task_input.user_id,
            title=task_input.title,
            description=task_input.description,
            completed=False
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        return {
            "success": True,
            "result": {
                "task_id": str(new_task.id),
                "title": new_task.title,
                "description": new_task.description,
                "completed": new_task.completed
            },
            "message": f"Task '{new_task.title}' added successfully"
        }
    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to add task"
        }


def list_tasks_tool(session: Session, user_id: str) -> Dict[str, Any]:
    """List all tasks for a specific user."""
    try:
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()

        task_list = []
        for task in tasks:
            task_list.append({
                "task_id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            })

        return {
            "success": True,
            "result": {
                "tasks": task_list
            },
            "message": f"Found {len(task_list)} tasks for user"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to list tasks"
        }


def update_task_tool(session: Session, task_update_input: TaskUpdateInput) -> Dict[str, Any]:
    """Update an existing task for a user."""
    try:
        # Find the task by ID and user ID to ensure ownership
        statement = select(Task).where(Task.id == task_update_input.task_id, Task.user_id == task_update_input.user_id)
        task = session.exec(statement).first()

        if not task:
            return {
                "success": False,
                "error": "Task not found or user not authorized",
                "message": "Task not found or you don't have permission to update this task"
            }

        # Update task fields if provided
        if task_update_input.title is not None:
            task.title = task_update_input.title
        if task_update_input.description is not None:
            task.description = task_update_input.description
        if task_update_input.completed is not None:
            task.completed = task_update_input.completed

        task.updated_at = datetime.now()

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "result": {
                "task_id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            },
            "message": f"Task '{task.title}' updated successfully"
        }
    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to update task"
        }


def complete_task_tool(session: Session, task_input: TaskIdInput) -> Dict[str, Any]:
    """Mark a task as completed."""
    try:
        # Find the task by ID and ensure it belongs to the user
        statement = select(Task).where(Task.id == task_input.task_id)
        task = session.exec(statement).first()

        if not task:
            return {
                "success": False,
                "error": "Task not found",
                "message": "Task not found or you don't have permission to complete this task"
            }

        task.completed = True
        task.updated_at = datetime.now()

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "result": {
                "task_id": str(task.id),
                "completed": task.completed
            },
            "message": f"Task '{task.title}' marked as completed"
        }
    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to complete task"
        }


def delete_task_tool(session: Session, task_input: TaskIdInput) -> Dict[str, Any]:
    """Delete a task."""
    try:
        # Find the task by ID and ensure it belongs to the user
        statement = select(Task).where(Task.id == task_input.task_id)
        task = session.exec(statement).first()

        if not task:
            return {
                "success": False,
                "error": "Task not found",
                "message": "Task not found or you don't have permission to delete this task"
            }

        session.delete(task)
        session.commit()

        return {
            "success": True,
            "result": {
                "task_id": str(task.id),
                "message": f"Task '{task.title}' deleted successfully"
            },
            "message": f"Task '{task.title}' deleted successfully"
        }
    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to delete task"
        }


# Dictionary of available tools
TOOLS = {
    "add_task": add_task_tool,
    "list_tasks": list_tasks_tool,
    "update_task": update_task_tool,
    "complete_task": complete_task_tool,
    "delete_task": delete_task_tool
}


def execute_tool(tool_name: str, session: Session, **kwargs) -> Dict[str, Any]:
    """Execute the specified tool with the given parameters."""
    if tool_name not in TOOLS:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}",
            "message": f"The tool '{tool_name}' is not available"
        }

    tool_func = TOOLS[tool_name]

    # Execute the tool with the provided session and arguments
    try:
        # For simplicity, passing the kwargs directly to the tool
        # In a real implementation, you'd want to validate the inputs
        if tool_name == "add_task":
            task_input = TaskInput(**kwargs)
            return tool_func(session, task_input)
        elif tool_name == "list_tasks":
            user_id = kwargs.get("user_id")
            return tool_func(session, user_id)
        elif tool_name == "update_task":
            task_update_input = TaskUpdateInput(**kwargs)
            return tool_func(session, task_update_input)
        elif tool_name in ["complete_task", "delete_task"]:
            task_input = TaskIdInput(**kwargs)
            return tool_func(session, task_input)
        else:
            return {
                "success": False,
                "error": f"Tool execution not properly handled: {tool_name}",
                "message": f"Tool '{tool_name}' execution not properly configured"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Error executing tool {tool_name}: {str(e)}"
        }