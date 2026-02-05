"""AI Agent service for processing natural language commands."""

import asyncio
from typing import Dict, Any, Optional
from sqlmodel import Session
from uuid import UUID
from openai import OpenAI
from database.config import settings

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ..models.conversation import Conversation
from ..models.message import Message
from .conversation_service import ConversationService
from .message_service import MessageService
from ..tools.mcp_tools import execute_tool, TOOLS


class AIAgentService:
    """Service class for handling AI agent operations."""

    def __init__(self):
        """Initialize the AI agent service with OpenAI client."""
        if settings.openai_api_key:
            self.client = OpenAI(api_key=settings.openai_api_key)
        else:
            # For development without OpenAI key, we'll use mock responses
            self.client = None
            print("Warning: OpenAI API key not configured. Using mock responses.")

    async def process_user_message(
        self,
        db: Session,
        user_id: str,
        conversation_id: UUID,
        user_message: str
    ) -> Dict[str, Any]:
        """
        Process a user message and return an appropriate AI response.

        Args:
            db: Database session
            user_id: ID of the requesting user
            conversation_id: ID of the conversation
            user_message: The message from the user

        Returns:
            Dictionary containing the AI response and any action results
        """
        try:
            # Get conversation history to provide context
            conversation_history = MessageService.get_messages_by_conversation(db, conversation_id)

            # Prepare the context for the AI
            messages_context = []
            for msg in conversation_history:
                role = "user" if msg.role.value == "user" else "assistant"
                messages_context.append({
                    "role": role,
                    "content": msg.content
                })

            # Add the new user message
            messages_context.append({
                "role": "user",
                "content": user_message
            })

            # If we have OpenAI configured, use it
            if self.client:
                return await self._process_with_openai(db, user_id, messages_context)
            else:
                # Use the rule-based approach as fallback
                return await self._process_with_rules(db, user_id, user_message)

        except Exception as e:
            print(f"Error in AI agent processing: {str(e)}")
            return {
                "response": "Sorry, I encountered an error processing your request.",
                "action_result": {
                    "type": "error",
                    "success": False,
                    "result": {"error": str(e)}
                }
            }

    async def _process_with_openai(
        self,
        db: Session,
        user_id: str,
        messages: list
    ) -> Dict[str, Any]:
        """Process message using OpenAI API with function calling."""
        try:
            # Define available functions (tools) that the AI can use
            functions = [
                {
                    "name": "add_task",
                    "description": "Add a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the task to add"
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional description of the task"
                            }
                        },
                        "required": ["title"]
                    }
                },
                {
                    "name": "list_tasks",
                    "description": "List all tasks for the user"
                },
                {
                    "name": "update_task",
                    "description": "Update an existing task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "The ID of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "The new title of the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "The new description of the task"
                            },
                            "completed": {
                                "type": "boolean",
                                "description": "Whether the task is completed"
                            }
                        },
                        "required": ["task_id"]
                    }
                },
                {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "The ID of the task to mark as completed"
                            }
                        },
                        "required": ["task_id"]
                    }
                },
                {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "The ID of the task to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            ]

            # Call OpenAI API with function calling
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                functions=functions,
                function_call="auto"
            )

            response_message = response.choices[0].message

            # Check if the model wanted to call a function
            if response_message.function_call:
                # Get the name and arguments of the function to call
                function_name = response_message.function_call.name
                function_args = response_message.function_call.arguments

                # Execute the appropriate tool
                import json
                args_dict = json.loads(function_args)

                # Add user_id to arguments for tools that need it
                if function_name in ["add_task", "list_tasks"]:
                    args_dict["user_id"] = user_id

                result = execute_tool(function_name, db, **args_dict)

                return {
                    "response": result.get("message", f"Action completed: {function_name}"),
                    "action_result": {
                        "type": function_name,
                        "success": result.get("success", False),
                        "result": result.get("result", {})
                    }
                }
            else:
                # If no function was called, return the model's response
                return {
                    "response": response_message.content or "I processed your request.",
                    "action_result": {
                        "type": "text_response",
                        "success": True,
                        "result": {"content": response_message.content}
                    }
                }

        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            # Fall back to rule-based processing
            return await self._process_with_rules(db, user_id, messages[-1]["content"])

    async def _process_with_rules(
        self,
        db: Session,
        user_id: str,
        message: str
    ) -> Dict[str, Any]:
        """
        Process message using rule-based approach as fallback.
        This replicates the logic from the chat route for consistency.
        """
        import re

        # Simple rule-based approach to identify user intent
        message_lower = message.lower().strip()

        # Pattern matching for different commands
        if "add task" in message_lower or "create task" in message_lower:
            # Extract task title using regex
            match = re.search(r'(?:add task|create task)[:\s]*(.+)', message_lower)
            if match:
                task_title = match.group(1).strip()

                # Prepare tool parameters
                tool_params = {
                    "title": task_title,
                    "user_id": user_id
                }

                # Execute the add_task tool
                result = execute_tool("add_task", db, **tool_params)

                return {
                    "response": result.get("message", f"I've added the task '{task_title}'."),
                    "action_result": {
                        "type": "add_task",
                        "success": result.get("success", False),
                        "result": result.get("result", {})
                    }
                }

        elif "show tasks" in message_lower or "list tasks" in message_lower or "my tasks" in message_lower:
            # Execute the list_tasks tool
            result = execute_tool("list_tasks", db, user_id=user_id)

            if result.get("success"):
                tasks = result["result"]["tasks"]
                if tasks:
                    task_list_str = ", ".join([f"'{task['title']}' ({'completed' if task['completed'] else 'pending'})" for task in tasks])
                    response_text = f"You have {len(tasks)} tasks: {task_list_str}."
                else:
                    response_text = "You don't have any tasks."
            else:
                response_text = "I couldn't retrieve your tasks."

            return {
                "response": response_text,
                "action_result": {
                    "type": "list_tasks",
                    "success": result.get("success", False),
                    "result": result.get("result", {})
                }
            }

        elif "complete task" in message_lower or "finish task" in message_lower:
            # Extract task identification
            match = re.search(r'(?:complete task|finish task)[:\s]*(.+)', message_lower)
            if match:
                task_identifier = match.group(1).strip()

                # First, list tasks to find the matching one
                list_result = execute_tool("list_tasks", db, user_id=user_id)
                if list_result.get("success"):
                    tasks = list_result["result"]["tasks"]

                    # Find the task to complete (match by title)
                    target_task = None
                    for task in tasks:
                        if task_identifier.lower() in task["title"].lower():
                            target_task = task
                            break

                    if target_task:
                        # Execute the complete_task tool
                        tool_params = {
                            "task_id": target_task["task_id"]
                        }
                        result = execute_tool("complete_task", db, **tool_params)

                        return {
                            "response": result.get("message", f"I've completed the task '{target_task['title']}'."),
                            "action_result": {
                                "type": "complete_task",
                                "success": result.get("success", False),
                                "result": result.get("result", {})
                            }
                        }
                    else:
                        return {
                            "response": f"I couldn't find a task matching '{task_identifier}'.",
                            "action_result": {
                                "type": "complete_task",
                                "success": False,
                                "result": {}
                            }
                        }
                else:
                    return {
                        "response": "I couldn't find your tasks to complete.",
                        "action_result": {
                            "type": "complete_task",
                            "success": False,
                            "result": {}
                        }
                    }

        elif "delete task" in message_lower:
            # Extract task identification
            match = re.search(r'delete task[:\s]*(.+)', message_lower)
            if match:
                task_identifier = match.group(1).strip()

                # First, list tasks to find the matching one
                list_result = execute_tool("list_tasks", db, user_id=user_id)
                if list_result.get("success"):
                    tasks = list_result["result"]["tasks"]

                    # Find the task to delete (match by title)
                    target_task = None
                    for task in tasks:
                        if task_identifier.lower() in task["title"].lower():
                            target_task = task
                            break

                    if target_task:
                        # Execute the delete_task tool
                        tool_params = {
                            "task_id": target_task["task_id"]
                        }
                        result = execute_tool("delete_task", db, **tool_params)

                        return {
                            "response": result.get("message", f"I've deleted the task '{target_task['title']}'."),
                            "action_result": {
                                "type": "delete_task",
                                "success": result.get("success", False),
                                "result": result.get("result", {})
                            }
                        }
                    else:
                        return {
                            "response": f"I couldn't find a task matching '{task_identifier}'.",
                            "action_result": {
                                "type": "delete_task",
                                "success": False,
                                "result": {}
                            }
                        }
                else:
                    return {
                        "response": "I couldn't find your tasks to delete.",
                        "action_result": {
                            "type": "delete_task",
                            "success": False,
                            "result": {}
                        }
                    }

        elif "update task" in message_lower or "edit task" in message_lower:
            # More complex - need to identify which task and what to update
            # Pattern: "update task 'original task' to 'new title'"
            match = re.search(r'(?:update task|edit task)\s*[\'"](.+?)[\'"]\s*(?:to|with)\s*[\'"](.+?)[\'"]', message)
            if not match:
                # Alternative pattern: "update task 'task title' and set description to 'new description'"
                match = re.search(r'(?:update task|edit task)\s*[\'"](.+?)[\'"](?:.*?(?:and|to|with)\s+(?:set\s+)?(?:title\s+to|description\s+to|desc\s+to)\s*[\'"](.+?)[\'"])', message)

            if match:
                original_title = match.group(1).strip()
                new_value = match.group(2).strip()

                # First, list tasks to find the matching one
                list_result = execute_tool("list_tasks", db, user_id=user_id)
                if list_result.get("success"):
                    tasks = list_result["result"]["tasks"]

                    # Find the task to update (match by title)
                    target_task = None
                    for task in tasks:
                        if original_title.lower() in task["title"].lower():
                            target_task = task
                            break

                    if target_task:
                        # Execute the update_task tool
                        tool_params = {
                            "task_id": target_task["task_id"],
                            "title": new_value  # For simplicity, assuming we're updating the title
                        }
                        result = execute_tool("update_task", db, **tool_params)

                        return {
                            "response": result.get("message", f"I've updated the task '{original_title}' to '{new_value}'."),
                            "action_result": {
                                "type": "update_task",
                                "success": result.get("success", False),
                                "result": result.get("result", {})
                            }
                        }
                    else:
                        return {
                            "response": f"I couldn't find a task matching '{original_title}'.",
                            "action_result": {
                                "type": "update_task",
                                "success": False,
                                "result": {}
                            }
                        }
                else:
                    return {
                        "response": f"I couldn't find the task '{original_title}' to update.",
                        "action_result": {
                            "type": "update_task",
                            "success": False,
                            "result": {}
                        }
                    }

        # Default response for unrecognized commands
        return {
            "response": f"I understood your message: '{message}'. I can help you manage tasks. Try commands like 'Add task: Buy groceries' or 'Show my tasks'.",
            "action_result": {
                "type": "unknown_command",
                "success": False,
                "result": {}
            }
        }