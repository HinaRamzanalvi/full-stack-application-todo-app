# API Contract: Chat Endpoint for AI-Powered Todo Chatbot

## Overview
This document defines the API contract for the chat endpoint that enables AI-powered task management through natural language commands.

## Endpoint: POST /api/chat

### Description
Processes natural language commands from users and performs corresponding task operations. The endpoint handles conversation context and returns appropriate responses based on the user's intent.

### Request

#### Headers
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

#### Request Body
```json
{
  "message": "string (required) - The user's message/command",
  "conversation_id": "string (optional) - ID of existing conversation to continue, or null for new conversation"
}
```

#### Example Request
```json
{
  "message": "Add task: Buy groceries",
  "conversation_id": null
}
```

### Response

#### Success Response (200 OK)
```json
{
  "success": true,
  "data": {
    "response": "string - AI's response to the user",
    "conversation_id": "string - ID of the conversation thread",
    "action_result": {
      "type": "string - Type of action performed (add_task, list_tasks, etc.)",
      "success": "boolean - Whether the action was successful",
      "result": "object - Details of the action result (varies by action type)"
    },
    "timestamp": "string - ISO 8601 timestamp of the response"
  }
}
```

#### Example Success Response
```json
{
  "success": true,
  "data": {
    "response": "I've added the task 'Buy groceries' to your list.",
    "conversation_id": "uuid-string-here",
    "action_result": {
      "type": "add_task",
      "success": true,
      "result": {
        "task_id": "uuid-string-here",
        "title": "Buy groceries",
        "completed": false
      }
    },
    "timestamp": "2026-01-28T10:30:00.000Z"
  }
}
```

#### Error Response (400 Bad Request)
```json
{
  "success": false,
  "error": {
    "code": "string - Error code",
    "message": "string - Human-readable error message",
    "details": "object - Additional error details if applicable"
  }
}
```

#### Example Error Response
```json
{
  "success": false,
  "error": {
    "code": "INVALID_COMMAND",
    "message": "Could not understand the command. Please try rephrasing."
  }
}
```

#### Authentication Error (401 Unauthorized)
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

### Action Result Types

#### add_task
```json
{
  "type": "add_task",
  "success": true,
  "result": {
    "task_id": "string - ID of the created task",
    "title": "string - Title of the task",
    "description": "string - Description if provided",
    "completed": false
  }
}
```

#### list_tasks
```json
{
  "type": "list_tasks",
  "success": true,
  "result": {
    "tasks": [
      {
        "task_id": "string",
        "title": "string",
        "description": "string",
        "completed": "boolean",
        "created_at": "string - ISO 8601 timestamp"
      }
    ]
  }
}
```

#### update_task
```json
{
  "type": "update_task",
  "success": true,
  "result": {
    "task_id": "string - ID of the updated task",
    "title": "string - Updated title",
    "description": "string - Updated description if provided",
    "completed": "boolean - Updated completion status"
  }
}
```

#### complete_task
```json
{
  "type": "complete_task",
  "success": true,
  "result": {
    "task_id": "string - ID of the completed task",
    "completed": true
  }
}
```

#### delete_task
```json
{
  "type": "delete_task",
  "success": true,
  "result": {
    "task_id": "string - ID of the deleted task",
    "message": "string - Confirmation message"
  }
}
```

## Security Requirements

1. **Authentication**: All requests must include a valid JWT token in the Authorization header
2. **Authorization**: Users can only access their own conversations and tasks
3. **Input Validation**: All user inputs must be validated and sanitized
4. **Rate Limiting**: Requests should be limited to prevent abuse

## Performance Requirements

1. **Response Time**: 95% of requests should respond within 2 seconds
2. **Availability**: Endpoint should be available 99.9% of the time
3. **Scalability**: Should handle at least 100 concurrent users

## Error Codes

- `UNAUTHORIZED`: Missing or invalid authentication token
- `INVALID_COMMAND`: AI could not understand the user's command
- `TASK_NOT_FOUND`: Requested task does not exist
- `INSUFFICIENT_PERMISSIONS`: User attempting to access another user's data
- `RATE_LIMIT_EXCEEDED`: Too many requests from the same user
- `INTERNAL_ERROR`: Unexpected server error occurred