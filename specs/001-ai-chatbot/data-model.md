# Data Model: AI-Powered Chatbot for Todo Management

## Entity Definitions

### Conversation
Represents a single chat session between user and AI.

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the conversation
- `user_id`: UUID (Foreign Key) - Links to the user who owns this conversation
- `created_at`: DateTime - Timestamp when conversation was initiated
- `updated_at`: DateTime - Timestamp of last activity in conversation

**Relationships**:
- Belongs to: User (many-to-one)
- Has many: Messages (one-to-many)

**Validation**:
- `user_id` must reference an existing user
- `created_at` is set automatically on creation
- `updated_at` is updated automatically on any changes

### Message
Represents an individual message in a conversation.

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the message
- `user_id`: UUID (Foreign Key) - Links to the user who sent this message
- `conversation_id`: UUID (Foreign Key) - Links to the conversation this message belongs to
- `role`: String (Enum: 'user' | 'assistant') - Identifies if message is from user or AI
- `content`: Text - The actual message content
- `created_at`: DateTime - Timestamp when message was created

**Relationships**:
- Belongs to: User (many-to-one)
- Belongs to: Conversation (many-to-one)

**Validation**:
- `user_id` must reference an existing user
- `conversation_id` must reference an existing conversation
- `role` must be either 'user' or 'assistant'
- `content` cannot be empty
- `created_at` is set automatically on creation

### Task (Reused from Phase 2)
Represents user tasks with additional relationships to conversations.

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the task
- `user_id`: UUID (Foreign Key) - Links to the user who owns this task
- `title`: String (Required) - Title of the task
- `description`: Text (Optional) - Detailed description of the task
- `completed`: Boolean - Whether the task is completed
- `created_at`: DateTime - Timestamp when task was created
- `updated_at`: DateTime - Timestamp of last update

**Relationships**:
- Belongs to: User (many-to-one)
- Referenced by: Messages (via conversation context)

**Validation**:
- `user_id` must reference an existing user
- `title` cannot be empty
- `completed` defaults to False

## State Transitions

### Task State Transitions
- **Incomplete → Complete**: When user marks task as complete via chat command
- **Complete → Incomplete**: When user marks task as incomplete via chat command

### Conversation State Transitions
- **Active**: When new messages are added to the conversation
- **Inactive**: When no new messages are added for a configured period (e.g., 24 hours)

## Data Relationships

```
User (1) ←→ (Many) Conversation (1) ←→ (Many) Message
User (1) ←→ (Many) Task
```

## Database Constraints

### Indexes
- `conversations.user_id`: For fast retrieval of user's conversations
- `messages.conversation_id`: For fast retrieval of messages in a conversation
- `messages.user_id`: For enforcing user data isolation
- `tasks.user_id`: For fast retrieval of user's tasks
- `tasks.completed`: For efficient filtering of completed/incomplete tasks

### Foreign Key Constraints
- `conversations.user_id` → `users.id`
- `messages.user_id` → `users.id`
- `messages.conversation_id` → `conversations.id`
- `tasks.user_id` → `users.id`

### Data Integrity Rules
- Cascade delete: When a user is deleted, their conversations and messages are also deleted
- When a conversation is deleted, all associated messages are deleted
- Tasks remain when conversations are deleted (they're independent entities)

## Query Patterns

### Common Queries
1. **Get user's conversations**: Filter by `user_id` in `conversations` table
2. **Get conversation messages**: Filter by `conversation_id` in `messages` table, ordered by `created_at`
3. **Get user's tasks**: Filter by `user_id` in `tasks` table
4. **Validate access**: Ensure `user_id` matches authenticated user for any requested resource

### Security Enforcement
- All queries must filter by `user_id` to enforce data isolation
- No queries should join across user boundaries without proper authorization