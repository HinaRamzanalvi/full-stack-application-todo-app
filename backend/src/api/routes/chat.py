"""Chat API routes for the AI-powered chatbot."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import time
from pydantic import BaseModel

from ...models.conversation import Conversation, ConversationCreate
from ...models.message import Message, MessageCreate, MessageRole
from ...services.conversation_service import ConversationService
from ...services.message_service import MessageService
from ...services.ai_agent_service import AIAgentService
from ...tools.mcp_tools import execute_tool
from ...api.deps import get_db_session, get_current_active_user
from middleware.auth import TokenData


# Simple rate limiting implementation
user_request_times = defaultdict(list)
RATE_LIMIT = 10  # max requests
RATE_WINDOW = 60  # per 60 seconds


def check_rate_limit(user_id: str) -> bool:
    """Check if user has exceeded rate limit."""
    current_time = time.time()

    # Remove requests older than the window
    user_request_times[user_id] = [
        req_time for req_time in user_request_times[user_id]
        if current_time - req_time < RATE_WINDOW
    ]

    # Check if user is within rate limit
    if len(user_request_times[user_id]) >= RATE_LIMIT:
        return False

    # Add current request time
    user_request_times[user_id].append(current_time)
    return True


router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    success: bool
    data: Dict[str, Any]


@router.post("/chat")
async def chat(
    request: ChatRequest,
    current_user: TokenData = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Process natural language commands from users and perform corresponding task operations.
    The endpoint handles conversation context and returns appropriate responses based on the user's intent.
    """
    try:
        user_id = current_user.user_id
        message = request.message
        conversation_id = request.conversation_id

        # Rate limiting
        if not check_rate_limit(user_id):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please slow down your requests."
            )

        # Input validation and sanitization
        if not message or not message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message cannot be empty"
            )

        # Sanitize input - strip leading/trailing whitespace and limit length
        message = message.strip()
        if len(message) > 1000:  # Limit message length to prevent abuse
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message is too long. Maximum length is 1000 characters."
            )

        # Additional sanitization could be added here if needed
        # For example, removing potential harmful characters or patterns

        # Log incoming request
        print(f"[LOG] Chat request from user {user_id[:8]}..., conversation: {conversation_id}, message: {message[:50]}...")

        # Get or create conversation
        conv_id: Optional[UUID] = None
        if conversation_id:
            try:
                conv_id = UUID(conversation_id)
                # Verify user has access to this conversation
                if not MessageService.validate_user_access_to_conversation(db, conv_id, user_id):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access denied to this conversation"
                    )
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid conversation ID format"
                )
        else:
            # Create a new conversation
            new_conv_data = ConversationCreate(user_id=user_id, title=message[:50] + "..." if len(message) > 50 else message)
            new_conv = ConversationService.create_conversation(db, new_conv_data)
            conv_id = new_conv.id

        if not conv_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to establish conversation"
            )

        # Save user message
        user_message = MessageCreate(
            user_id=user_id,
            conversation_id=conv_id,
            role=MessageRole.USER,
            content=message
        )
        saved_user_msg = MessageService.create_message(db, user_message)

        # Process the message with AI agent
        ai_agent = AIAgentService()
        ai_response = await ai_agent.process_user_message(db, user_id, conv_id, message)

        # Save AI response
        ai_message = MessageCreate(
            user_id=user_id,  # AI responses are associated with the user's conversation
            conversation_id=conv_id,
            role=MessageRole.ASSISTANT,
            content=ai_response.get("response", "I couldn't process that request.")
        )
        saved_ai_msg = MessageService.create_message(db, ai_message)

        # Update conversation timestamp
        ConversationService.update_conversation_timestamp(db, conv_id)

        # Prepare response
        response_data = {
            "response": ai_response.get("response", "I processed your request."),
            "conversation_id": str(conv_id),
            "action_result": ai_response.get("action_result", {}),
            "timestamp": datetime.now().isoformat()
        }

        # Log successful response
        print(f"[LOG] Chat response for user {user_id[:8]}..., conversation: {conv_id}, action: {ai_response.get('action_result', {}).get('type', 'unknown')}")

        return {
            "success": True,
            "data": response_data
        }

    except HTTPException as e:
        # Log HTTP exceptions
        print(f"[ERROR] HTTP exception in chat endpoint: {e.detail}")
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log unexpected errors
        print(f"[ERROR] Chat endpoint error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred while processing chat request"
        )


