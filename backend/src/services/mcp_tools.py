"""
MCP tools for task operations in the AI chatbot.
These tools allow the AI agent to perform task operations through natural language commands.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from ..models.task import Task
from uuid import UUID


class AddTaskInput(BaseModel):
    """Input schema for adding a new task."""
    title: str = Field(..., description="Title of the task to create")
    description: Optional[str] = Field(None, description="Description of the task")
    user_id: str = Field(..., description="ID of the user creating the task")


class ListTasksInput(BaseModel):
    """Input schema for listing tasks."""
    user_id: str = Field(..., description="ID of the user whose tasks to list")
    completed: Optional[bool] = Field(None, description="Filter by completion status if specified")


class UpdateTaskInput(BaseModel):
    """Input schema for updating a task."""
    task_id: str = Field(..., description="ID of the task to update")
    title: Optional[str] = Field(None, description="New title for the task")
    description: Optional[str] = Field(None, description="New description for the task")
    completed: Optional[bool] = Field(None, description="New completion status for the task")
    user_id: str = Field(..., description="ID of the user who owns the task")


class CompleteTaskInput(BaseModel):
    """Input schema for completing a task."""
    task_id: str = Field(..., description="ID of the task to complete")
    user_id: str = Field(..., description="ID of the user who owns the task")


class DeleteTaskInput(BaseModel):
    """Input schema for deleting a task."""
    task_id: str = Field(..., description="ID of the task to delete")
    user_id: str = Field(..., description="ID of the user who owns the task")


class MCPTaskService:
    """Service class containing MCP tools for task operations."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_task(self, input_data: AddTaskInput) -> Dict[str, Any]:
        """Add a new task for the user."""
        try:
            # Create new task
            task = Task(
                title=input_data.title,
                description=input_data.description,
                user_id=input_data.user_id,
                completed=False  # Default to not completed
            )

            # Add to database
            self.db_session.add(task)
            self.db_session.commit()
            self.db_session.refresh(task)

            return {
                "success": True,
                "result": {
                    "task_id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                }
            }
        except Exception as e:
            self.db_session.rollback()
            return {
                "success": False,
                "error": f"Failed to add task: {str(e)}"
            }

    def list_tasks(self, input_data: ListTasksInput) -> Dict[str, Any]:
        """List tasks for the user with optional filtering."""
        try:
            # Build query
            query = select(Task).where(Task.user_id == input_data.user_id)

            # Apply completion filter if specified
            if input_data.completed is not None:
                query = query.where(Task.completed == input_data.completed)

            # Execute query
            tasks = self.db_session.exec(query).all()

            # Format results
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
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to list tasks: {str(e)}"
            }

    def update_task(self, input_data: UpdateTaskInput) -> Dict[str, Any]:
        """Update an existing task for the user."""
        try:
            # Find the task
            task_id = UUID(input_data.task_id) if isinstance(input_data.task_id, str) else input_data.task_id
            statement = select(Task).where(Task.id == task_id, Task.user_id == input_data.user_id)
            task = self.db_session.exec(statement).first()

            if not task:
                return {
                    "success": False,
                    "error": f"Task with ID {input_data.task_id} not found or does not belong to user"
                }

            # Update fields that were provided
            if input_data.title is not None:
                task.title = input_data.title
            if input_data.description is not None:
                task.description = input_data.description
            if input_data.completed is not None:
                task.completed = input_data.completed

            # Update timestamp
            task.updated_at = Task.get_current_time()

            # Commit changes
            self.db_session.add(task)
            self.db_session.commit()
            self.db_session.refresh(task)

            return {
                "success": True,
                "result": {
                    "task_id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                }
            }
        except Exception as e:
            self.db_session.rollback()
            return {
                "success": False,
                "error": f"Failed to update task: {str(e)}"
            }

    def complete_task(self, input_data: CompleteTaskInput) -> Dict[str, Any]:
        """Mark a task as completed for the user."""
        try:
            # Find the task
            task_id = UUID(input_data.task_id) if isinstance(input_data.task_id, str) else input_data.task_id
            statement = select(Task).where(Task.id == task_id, Task.user_id == input_data.user_id)
            task = self.db_session.exec(statement).first()

            if not task:
                return {
                    "success": False,
                    "error": f"Task with ID {input_data.task_id} not found or does not belong to user"
                }

            # Update completion status
            task.completed = True
            task.updated_at = Task.get_current_time()

            # Commit changes
            self.db_session.add(task)
            self.db_session.commit()
            self.db_session.refresh(task)

            return {
                "success": True,
                "result": {
                    "task_id": str(task.id),
                    "completed": task.completed
                }
            }
        except Exception as e:
            self.db_session.rollback()
            return {
                "success": False,
                "error": f"Failed to complete task: {str(e)}"
            }

    def delete_task(self, input_data: DeleteTaskInput) -> Dict[str, Any]:
        """Delete a task for the user."""
        try:
            # Find the task
            task_id = UUID(input_data.task_id) if isinstance(input_data.task_id, str) else input_data.task_id
            statement = select(Task).where(Task.id == task_id, Task.user_id == input_data.user_id)
            task = self.db_session.exec(statement).first()

            if not task:
                return {
                    "success": False,
                    "error": f"Task with ID {input_data.task_id} not found or does not belong to user"
                }

            # Delete the task
            self.db_session.delete(task)
            self.db_session.commit()

            return {
                "success": True,
                "result": {
                    "task_id": str(task.id),
                    "message": "Task deleted successfully"
                }
            }
        except Exception as e:
            self.db_session.rollback()
            return {
                "success": False,
                "error": f"Failed to delete task: {str(e)}"
            }


# Tool definitions that can be registered with the AI agent
def create_add_task_tool(task_service: MCPTaskService):
    """Create the add_task tool function."""
    def add_task(title: str, description: Optional[str] = None, user_id: str = None):
        input_data = AddTaskInput(title=title, description=description, user_id=user_id)
        return task_service.add_task(input_data)
    return add_task


def create_list_tasks_tool(task_service: MCPTaskService):
    """Create the list_tasks tool function."""
    def list_tasks(user_id: str, completed: Optional[bool] = None):
        input_data = ListTasksInput(user_id=user_id, completed=completed)
        return task_service.list_tasks(input_data)
    return list_tasks


def create_update_task_tool(task_service: MCPTaskService):
    """Create the update_task tool function."""
    def update_task(task_id: str, user_id: str, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None):
        input_data = UpdateTaskInput(task_id=task_id, user_id=user_id, title=title, description=description, completed=completed)
        return task_service.update_task(input_data)
    return update_task


def create_complete_task_tool(task_service: MCPTaskService):
    """Create the complete_task tool function."""
    def complete_task(task_id: str, user_id: str):
        input_data = CompleteTaskInput(task_id=task_id, user_id=user_id)
        return task_service.complete_task(input_data)
    return complete_task


def create_delete_task_tool(task_service: MCPTaskService):
    """Create the delete_task tool function."""
    def delete_task(task_id: str, user_id: str):
        input_data = DeleteTaskInput(task_id=task_id, user_id=user_id)
        return task_service.delete_task(input_data)
    return delete_task