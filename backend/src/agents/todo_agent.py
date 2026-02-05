"""
OpenAI agent for todo operations with MCP tools integration.
"""

import os
from typing import Dict, Any, Optional
from openai import OpenAI
from sqlmodel import Session

from ..services.mcp_tools import MCPTaskService, create_add_task_tool, create_list_tasks_tool, create_update_task_tool, create_complete_task_tool, create_delete_task_tool


class TodoAgent:
    """
    AI agent that processes natural language commands and maps them to task operations
    using MCP tools for task management.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.task_service = MCPTaskService(db_session)

        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = OpenAI(api_key=api_key)

        # Create tool functions
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Title of the task to create"},
                            "description": {"type": "string", "description": "Description of the task"},
                            "user_id": {"type": "string", "description": "ID of the user creating the task"}
                        },
                        "required": ["title", "user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List tasks for the user with optional filtering",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "ID of the user whose tasks to list"},
                            "completed": {"type": "boolean", "description": "Filter by completion status if specified"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "ID of the task to update"},
                            "user_id": {"type": "string", "description": "ID of the user who owns the task"},
                            "title": {"type": "string", "description": "New title for the task"},
                            "description": {"type": "string", "description": "New description for the task"},
                            "completed": {"type": "boolean", "description": "New completion status for the task"}
                        },
                        "required": ["task_id", "user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "ID of the task to complete"},
                            "user_id": {"type": "string", "description": "ID of the user who owns the task"}
                        },
                        "required": ["task_id", "user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "ID of the task to delete"},
                            "user_id": {"type": "string", "description": "ID of the user who owns the task"}
                        },
                        "required": ["task_id", "user_id"]
                    }
                }
            }
        ]

    def process_message(self, message: str, user_id: str, conversation_context: Optional[list] = None) -> Dict[str, Any]:
        """
        Process a user message using OpenAI and MCP tools.

        Args:
            message: The user's message/command
            user_id: The ID of the user sending the message
            conversation_context: Previous conversation history (for context)

        Returns:
            Dictionary containing the response and any action results
        """
        try:
            # Prepare the messages for the OpenAI API
            messages = [{"role": "system", "content": """You are a helpful AI assistant that helps users manage their tasks.
                When a user gives you a task-related command, identify the appropriate action and call the relevant function.
                The available functions are:
                - add_task: Use this to add a new task. Extract the title and optional description from the user's message.
                - list_tasks: Use this to list the user's tasks.
                - update_task: Use this to update an existing task.
                - complete_task: Use this to mark a task as completed.
                - delete_task: Use this to delete a task.

                Always call the most appropriate function based on the user's request."""}]

            # Add conversation context if provided
            if conversation_context:
                messages.extend(conversation_context)

            # Add the current user message
            messages.append({"role": "user", "content": message})

            # Call the OpenAI API with function calling
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can change this to gpt-4 if preferred
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            # Get the response
            response_message = response.choices[0].message

            # Check if the model wanted to call a function
            tool_calls = response_message.tool_calls

            if tool_calls:
                # Process each tool call
                tool_results = []

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = eval(tool_call.function.arguments)

                    # Add user_id to the function arguments if not present
                    if "user_id" not in function_args:
                        function_args["user_id"] = user_id

                    # Call the appropriate function
                    if function_name == "add_task":
                        result = self.task_service.add_task(self.task_service.AddTaskInput(**function_args))
                    elif function_name == "list_tasks":
                        result = self.task_service.list_tasks(self.task_service.ListTasksInput(**function_args))
                    elif function_name == "update_task":
                        result = self.task_service.update_task(self.task_service.UpdateTaskInput(**function_args))
                    elif function_name == "complete_task":
                        result = self.task_service.complete_task(self.task_service.CompleteTaskInput(**function_args))
                    elif function_name == "delete_task":
                        result = self.task_service.delete_task(self.task_service.DeleteTaskInput(**function_args))
                    else:
                        result = {"success": False, "error": f"Unknown function: {function_name}"}

                    # Format the tool result
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(result)
                    })

                # Send the tool results back to the model
                messages.append(response_message)
                messages.extend(tool_results)

                # Get the final response from the model
                final_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )

                final_content = final_response.choices[0].message.content

                # Extract the action results from our tool calls
                action_result = {
                    "type": function_name,
                    "success": result.get("success", False),
                    "result": result.get("result", {})
                }

                return {
                    "response": final_content,
                    "action_result": action_result,
                    "success": True
                }
            else:
                # If no tool was called, return the model's response
                return {
                    "response": response_message.content,
                    "action_result": {
                        "type": "unknown",
                        "success": False,
                        "result": {}
                    },
                    "success": True
                }

        except Exception as e:
            # Handle any errors
            error_message = f"Sorry, I encountered an error processing your request: {str(e)}"
            return {
                "response": error_message,
                "action_result": {
                    "type": "error",
                    "success": False,
                    "error": str(e)
                },
                "success": False
            }


# Import the required classes for the type hints to work properly
try:
    from ..services.mcp_tools import AddTaskInput, ListTasksInput, UpdateTaskInput, CompleteTaskInput, DeleteTaskInput
except ImportError:
    # Define placeholder classes if imports fail
    class AddTaskInput:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    class ListTasksInput:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    class UpdateTaskInput:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    class CompleteTaskInput:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    class DeleteTaskInput:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)