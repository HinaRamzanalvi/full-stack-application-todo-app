# Data Model: Hackathon II Todo – Phase II: Full-Stack Web Application

## Entity: User
**Description**: Represents an authenticated user in the system
**Managed by**: Better Auth (external service)

**Attributes**:
- id: string (unique identifier, primary key)
- email: string (unique, required for authentication)
- name: string (optional, user display name)
- created_at: datetime (timestamp of account creation)
- updated_at: datetime (timestamp of last update)

**Relationships**:
- Has many: Task (via user_id foreign key)

## Entity: Task
**Description**: Represents a todo item created by a user

**Attributes**:
- id: integer (auto-incrementing primary key)
- user_id: string (foreign key to User.id, required)
- title: string (required, max length 255)
- description: string (optional, max length 1000)
- completed: boolean (default false)
- created_at: datetime (timestamp of creation, auto-generated)
- updated_at: datetime (timestamp of last update, auto-generated)

**Validation Rules**:
- title must not be empty
- user_id must reference an existing User
- created_at and updated_at are automatically managed

**State Transitions**:
- New task: completed = false (default)
- Task completed: completed = true
- Task uncompleted: completed = false

**Relationships**:
- Belongs to: User (via user_id foreign key)

## Database Schema

### Table: tasks
```
id: INTEGER (PRIMARY KEY, AUTO_INCREMENT)
user_id: STRING (FOREIGN KEY REFERENCES users.id, NOT NULL, INDEXED)
title: STRING (NOT NULL, MAX 255 CHARACTERS)
description: STRING (OPTIONAL, MAX 1000 CHARACTERS)
completed: BOOLEAN (DEFAULT FALSE, INDEXED)
created_at: DATETIME (NOT NULL, AUTO-GENERATED)
updated_at: DATETIME (NOT NULL, AUTO-GENERATED)
```

### Indexes:
- Index on user_id (for efficient user-based queries)
- Index on completed (for efficient filtering by completion status)
- Composite index on (user_id, completed) for optimized combined queries

## API Data Contracts

### Task Creation Request
```
{
  "title": "string (required, max 255 chars)",
  "description": "string (optional, max 1000 chars)"
}
```

### Task Response
```
{
  "id": "integer",
  "user_id": "string",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "created_at": "ISO 8601 datetime string",
  "updated_at": "ISO 8601 datetime string"
}
```

### Task Update Request
```
{
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

### Task List Response
```
{
  "tasks": [
    {
      // Same structure as Task Response
    }
  ],
  "total": "integer (total count)",
  "page": "integer (current page)",
  "limit": "integer (items per page)"
}
```