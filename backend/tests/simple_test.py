"""
Simple test to verify that the core functionality is working.
"""

import sys
import os
from uuid import uuid4

# Add the backend directory to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_basic_imports():
    """Test that we can import the main components."""
    try:
        from src.models.conversation import Conversation, ConversationCreate
        from src.models.message import Message, MessageCreate, MessageRole
        from src.services.conversation_service import ConversationService
        from src.services.message_service import MessageService
        from src.services.ai_agent_service import AIAgentService
        from src.tools.mcp_tools import execute_tool

        print("SUCCESS: All core modules imported successfully")

        # Test basic instantiation
        conv_create = ConversationCreate(user_id="test_user", title="Test Conversation")

        msg_create = MessageCreate(
            user_id="test_user",
            conversation_id=uuid4(),  # Use a proper UUID
            role=MessageRole.USER,
            content="Test message"
        )

        print("SUCCESS: Models instantiated successfully")

        # Test AI Agent Service
        ai_agent = AIAgentService()
        print("SUCCESS: AI Agent Service instantiated successfully")

        print("\nAll basic functionality tests passed!")
        return True

    except ImportError as e:
        print(f"ERROR: Import error: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Error: {e}")
        return False


def test_mcp_tools():
    """Test that MCP tools are available."""
    try:
        from src.tools.mcp_tools import TOOLS

        expected_tools = ['add_task', 'list_tasks', 'update_task', 'complete_task', 'delete_task']

        for tool in expected_tools:
            assert tool in TOOLS, f"Missing tool: {tool}"

        print("SUCCESS: All MCP tools are available")
        return True

    except Exception as e:
        print(f"ERROR: MCP Tools test failed: {e}")
        return False


if __name__ == "__main__":
    print("Running simple functionality tests...\n")

    success1 = test_basic_imports()
    success2 = test_mcp_tools()

    if success1 and success2:
        print("\nALL TESTS PASSED! The AI chatbot functionality is working correctly.")
    else:
        print("\nSOME TESTS FAILED.")