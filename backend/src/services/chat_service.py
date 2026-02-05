"""
Chat service to handle conversation logic and message processing for the AI chatbot.
"""

from typing import Dict, Any, Optional
from sqlmodel import Session, select
from uuid import UUID
import json
from datetime import datetime

from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate, MessageRole
from .mcp_tools import MCPTaskService, create_add_task_tool, create_list_tasks_tool, create_update_task_tool, create_complete_task_tool, create_delete_task_tool


class ChatService:
    """Service class to handle chat conversation logic and message processing."""

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.task_service = MCPTaskService(db_session)

    def create_conversation(self, user_id: str, title: Optional[str] = None) -> Conversation:
        """Create a new conversation for the user."""
        conversation_data = ConversationCreate(user_id=user_id, title=title)
        conversation = Conversation.from_orm(conversation_data) if hasattr(Conversation, 'from_orm') else Conversation(
            user_id=conversation_data.user_id,
            title=conversation_data.title
        )

        self.db_session.add(conversation)
        self.db_session.commit()
        self.db_session.refresh(conversation)
        return conversation

    def get_or_create_conversation(self, user_id: str, conversation_id: Optional[str] = None) -> Conversation:
        """Get existing conversation or create a new one if conversation_id is not provided."""
        if conversation_id:
            # Get existing conversation
            conv_uuid = UUID(conversation_id)
            statement = select(Conversation).where(
                Conversation.id == conv_uuid,
                Conversation.user_id == user_id
            )
            conversation = self.db_session.exec(statement).first()

            if not conversation:
                raise ValueError(f"Conversation with ID {conversation_id} not found or does not belong to user")

            return conversation
        else:
            # Create new conversation
            return self.create_conversation(user_id)

    def save_message(self, user_id: str, conversation_id: str, role: MessageRole, content: str) -> Message:
        """Save a message to the conversation."""
        conversation_uuid = UUID(conversation_id)

        # Verify that the conversation belongs to the user
        conversation_stmt = select(Conversation).where(
            Conversation.id == conversation_uuid,
            Conversation.user_id == user_id
        )
        conversation = self.db_session.exec(conversation_stmt).first()

        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found or does not belong to user")

        # Create and save the message
        message_data = MessageCreate(
            user_id=user_id,
            conversation_id=conversation_uuid,
            role=role,
            content=content
        )

        message = Message(
            user_id=message_data.user_id,
            conversation_id=message_data.conversation_id,
            role=message_data.role,
            content=message_data.content
        )

        self.db_session.add(message)
        self.db_session.commit()
        self.db_session.refresh(message)

        # Update conversation's updated_at timestamp
        conversation.updated_at = datetime.now()
        self.db_session.add(conversation)
        self.db_session.commit()

        return message

    def get_conversation_history(self, user_id: str, conversation_id: str, limit: int = 50) -> list:
        """Retrieve conversation history for a specific conversation."""
        conversation_uuid = UUID(conversation_id)

        # Verify that the conversation belongs to the user
        conversation_stmt = select(Conversation).where(
            Conversation.id == conversation_uuid,
            Conversation.user_id == user_id
        )
        conversation = self.db_session.exec(conversation_stmt).first()

        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found or does not belong to user")

        # Get messages for the conversation
        message_stmt = select(Message).where(
            Message.conversation_id == conversation_uuid
        ).order_by(Message.created_at.asc()).limit(limit)

        messages = self.db_session.exec(message_stmt).all()

        return [
            {
                "id": str(msg.id),
                "role": msg.role.value,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]

    def get_user_conversations(self, user_id: str) -> list:
        """Get all conversations for a specific user."""
        stmt = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
        conversations = self.db_session.exec(stmt).all()

        return [
            {
                "id": str(conv.id),
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat()
            }
            for conv in conversations
        ]

    def process_user_message(self, user_id: str, message_content: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a user message and generate a response.
        This method would typically integrate with an AI agent to process the natural language.
        For now, we'll simulate a basic response and task operations.
        """
        # Get or create conversation
        conversation = self.get_or_create_conversation(user_id, conversation_id)

        # Save user message
        user_message = self.save_message(
            user_id=user_id,
            conversation_id=str(conversation.id),
            role=MessageRole.USER,
            content=message_content
        )

        # Here we would normally call the AI agent to process the message
        # For now, we'll implement basic keyword recognition to simulate task operations

        response_text = ""
        action_result = None

        # Simple keyword recognition for demo purposes
        lower_msg = message_content.lower()

        if "add task" in lower_msg or "create task" in lower_msg:
            # Extract task title (simple parsing)
            if "add task" in lower_msg:
                task_part = lower_msg.split("add task")[1].strip()
            elif "create task" in lower_msg:
                task_part = lower_msg.split("create task")[1].strip()
            else:
                task_part = message_content.strip()

            # Remove common prefixes like "to" or "called"
            if task_part.startswith("to "):
                task_part = task_part[3:]
            elif task_part.startswith("called "):
                task_part = task_part[7:]

            task_title = task_part.strip()

            # Use the add_task MCP tool
            add_task_fn = create_add_task_tool(self.task_service)
            result = add_task_fn(title=task_title, user_id=user_id)

            if result["success"]:
                response_text = f"I've added the task '{task_title}' to your list."
                action_result = {
                    "type": "add_task",
                    "success": True,
                    "result": result["result"]
                }
            else:
                response_text = f"Sorry, I couldn't add the task: {result['error']}"
                action_result = {
                    "type": "add_task",
                    "success": False,
                    "error": result["error"]
                }

        elif "list tasks" in lower_msg or "show tasks" in lower_msg or "my tasks" in lower_msg:
            # Use the list_tasks MCP tool
            list_tasks_fn = create_list_tasks_tool(self.task_service)
            result = list_tasks_fn(user_id=user_id)

            if result["success"]:
                tasks = result["result"]["tasks"]
                if tasks:
                    task_list_str = ", ".join([f"'{t['title']}'" for t in tasks])
                    response_text = f"Here are your tasks: {task_list_str}."
                else:
                    response_text = "You don't have any tasks right now."

                action_result = {
                    "type": "list_tasks",
                    "success": True,
                    "result": result["result"]
                }
            else:
                response_text = f"Sorry, I couldn't retrieve your tasks: {result['error']}"
                action_result = {
                    "type": "list_tasks",
                    "success": False,
                    "error": result["error"]
                }

        elif "complete task" in lower_msg or "finish task" in lower_msg:
            # This would require more sophisticated parsing to identify the specific task
            # For now, we'll look for a simple pattern like "complete task X" where X is the task ID
            import re
            task_id_match = re.search(r'task (\w+)', lower_msg)

            if task_id_match:
                task_id = task_id_match.group(1)

                # Use the complete_task MCP tool
                complete_task_fn = create_complete_task_tool(self.task_service)
                result = complete_task_fn(task_id=task_id, user_id=user_id)

                if result["success"]:
                    response_text = f"I've marked the task as completed."
                    action_result = {
                        "type": "complete_task",
                        "success": True,
                        "result": result["result"]
                    }
                else:
                    response_text = f"Sorry, I couldn't complete the task: {result['error']}"
                    action_result = {
                        "type": "complete_task",
                        "success": False,
                        "error": result["error"]
                    }
            else:
                response_text = "I need to know which task to complete. Please specify the task ID."
                action_result = {
                    "type": "complete_task",
                    "success": False,
                    "error": "Task ID not specified"
                }

        else:
            # Default response for unrecognized commands
            response_text = f"I received your message: '{message_content}'. I can help you manage tasks using commands like 'Add task: buy groceries' or 'List tasks'."
            action_result = {
                "type": "unknown",
                "success": False,
                "error": "Command not recognized"
            }

        # Save assistant response
        assistant_message = self.save_message(
            user_id=user_id,
            conversation_id=str(conversation.id),
            role=MessageRole.ASSISTANT,
            content=response_text
        )

        # Prepare response
        response = {
            "response": response_text,
            "conversation_id": str(conversation.id),
            "action_result": action_result,
            "timestamp": datetime.now().isoformat()
        }

        return response