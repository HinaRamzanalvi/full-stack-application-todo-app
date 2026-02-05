# Quickstart Guide: AI-Powered Chatbot for Todo Management

## Overview
This guide provides essential information for developers to quickly understand and contribute to the AI chatbot feature implementation.

## Prerequisites

### Environment Setup
1. Node.js 18+ and npm/yarn for frontend development
2. Python 3.11+ with pip for backend development
3. PostgreSQL database (Neon Serverless recommended)
4. OpenAI API key for AI functionality
5. Better Auth configuration for user authentication

### Required Dependencies
- Frontend: Next.js 16+, TypeScript, Tailwind CSS
- Backend: FastAPI, SQLModel, OpenAI Python SDK
- Testing: pytest, Jest, React Testing Library

## Running the Application

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export DATABASE_URL="your_postgres_connection_string"
   export OPENAI_API_KEY="your_openai_api_key"
   export BETTER_AUTH_SECRET="your_auth_secret"
   ```

4. Run database migrations:
   ```bash
   python -m src.db.migrate
   ```

5. Start the backend server:
   ```bash
   uvicorn src.api.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set environment variables:
   ```bash
   NEXT_PUBLIC_API_URL="http://localhost:8000"
   NEXT_PUBLIC_OPENAI_DOMAIN_KEY="your_domain_key"
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## Key Components

### Backend Components
- `src/models/conversation.py`: Conversation data model
- `src/models/message.py`: Message data model
- `src/services/ai_agent_service.py`: AI processing logic
- `src/tools/mcp_tools.py`: MCP tools for task operations
- `src/api/routes/chat.py`: Chat API endpoint

### Frontend Components
- `src/components/ChatBot.tsx`: Main chat interface component
- `src/lib/api.ts`: Updated API client with chat functionality

## API Endpoints

### Chat Endpoint
- **POST** `/api/chat`
- Headers: `Authorization: Bearer {jwt_token}`
- Request Body: `{ "message": "user's message", "conversation_id": "optional existing conversation ID" }`
- Response: `{ "response": "AI response", "conversation_id": "conversation ID", "action_result": "optional result of task operation" }`

### Existing Task Endpoints
All existing task endpoints remain unchanged and continue to function as in Phase 2.

## Development Workflow

### Adding New MCP Tools
1. Add the new tool function in `src/tools/mcp_tools.py`
2. Register the tool with the AI agent service
3. Ensure proper authentication and user isolation
4. Add corresponding tests

### Modifying Chat Component
1. Update the UI in `src/components/ChatBot.tsx`
2. Adjust API calls in the frontend API client
3. Ensure responsive design with Tailwind CSS
4. Add/update frontend tests

### Database Changes
1. Update the model in the appropriate model file
2. Create a new migration
3. Update related services to handle new fields
4. Update tests to account for new functionality

## Testing

### Backend Tests
Run all backend tests:
```bash
pytest
```

Test chat functionality specifically:
```bash
pytest tests/test_chat.py
```

### Frontend Tests
Run all frontend tests:
```bash
npm test
```

Test chat component specifically:
```bash
npm test -- --testPathPattern=ChatBot
```

## Common Tasks

### Starting a New Conversation
1. Call POST `/api/chat` without conversation_id
2. AI agent will create a new conversation
3. Response includes new conversation_id for continuation

### Processing User Commands
1. User sends command like "Add task: Buy groceries"
2. AI agent parses the command
3. MCP tools execute the appropriate task operation
4. Result is returned to the user through the chat interface

### Retrieving Chat History
1. Conversation history is automatically loaded when the chat component mounts
2. Most recent conversation is loaded by default
3. Users can switch between conversation threads if multiple exist

## Troubleshooting

### Authentication Issues
- Verify JWT token is properly attached to all requests
- Check that BETTER_AUTH_SECRET matches between frontend and backend
- Ensure user is properly authenticated before accessing chat features

### AI Service Issues
- Confirm OPENAI_API_KEY is properly set
- Check API rate limits if experiencing delays
- Verify proper error handling when AI service is unavailable

### Database Connection Issues
- Ensure DATABASE_URL is correctly configured
- Verify database migrations have been applied
- Check that foreign key relationships are properly maintained