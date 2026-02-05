<!-- SYNC IMPACT REPORT
Version change: 1.2.0 → 1.3.0
Modified principles:
- Updated Chat Interface Design to include floating chatbot icon requirements
- Enhanced AI Integration Principles with specific UI/UX requirements
- Added Interactive Chatbot Requirements section
Added sections: Interactive Chatbot Requirements, Floating Chatbot UI Design, Real-Time Interaction Design
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->
# Hackathon III AI-Powered Todo Chatbot Constitution

## Core Principles

### Spec-Driven Development
Every change starts with updating or referencing specs in `/specs/`. Use `@specs/path/to/file.md` for references. Specs are organized by type: features, api, database, ui. Never implement without a spec.

### Monorepo Structure
Maintain the exact folder structure from documentation: `/specs/` with subfolders (features/, api/, database/, ui/), `/frontend/` (Next.js), `/backend/` (FastAPI), Root `CLAUDE.md`, `frontend/CLAUDE.md`, `backend/CLAUDE.md` for guidelines. `.spec-kit/config.yaml` with defined phases (phase3-chatbot extends phase2-web with ai-integration). Build Phase 3 within existing Phase 2 codebase - no new project structure.

### Technology Stack Compliance
Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS. Server components default; client components only for interactivity. No inline styles. Backend: Python FastAPI, SQLModel ORM, Neon Serverless PostgreSQL. Auth: Better Auth (frontend) with JWT plugin enabled. Shared `BETTER_AUTH_SECRET` env variable for signing/verification. API: RESTful, JSON responses, Pydantic models. AI Integration: OpenAI Agents SDK for natural language understanding and MCP tools for task operations.

### Security and Authentication (Mandatory for ALL Endpoints)
Stateless JWT authentication: Frontend issues JWT on login/signup; attach to every API request in `Authorization: Bearer <token>` header. Backend: Middleware to verify JWT signature with shared secret, extract user_id, and enforce on every route. 401 Unauthorized for missing/invalid/expired tokens. Data Isolation: EVERY database query MUST filter by authenticated `user_id` (e.g., `WHERE user_id = current_user_id`). No cross-user data access. Token Expiry: Default 7 days; configurable but always enforce expiry. Users table managed by Better Auth; tasks have `user_id` foreign key. Chatbot access restricted to authenticated users only.

### API Design
Updated endpoints (stateless, no {user_id} in path): GET /api/tasks (list with filters: status, sort), POST /api/tasks, GET /api/tasks/{id}, PUT /api/tasks/{id}, DELETE /api/tasks/{id}, PATCH /api/tasks/{id}/complete (toggle). NEW: POST /api/chat (chatbot interaction endpoint). Use proper HTTP methods, status codes, error handling (HTTPException). Filter responses to authenticated user's tasks only. All chatbot operations must respect user authentication and data isolation.

### Database Rules
Schema exactly as in `/specs/database/schema.md`: users (Better Auth), tasks (id, user_id FK, title, description, completed, timestamps). NEW: conversations (id, user_id FK, created_at, updated_at), messages (id, conversation_id FK, role, content, timestamp). Indexes on user_id and completed for tasks; indexes on user_id and conversation_id for chat data. Use SQLModel for models, queries, sessions. Connection via `DATABASE_URL` env. Store chat history in database tables, not in server memory. Keep system stateless at server level.

### Frontend Patterns
API client in `/lib/api.ts`: Attach JWT to all requests. Responsive UI with Tailwind. Pages: Login/Signup, Task list (filter/sort), Create/Edit forms. NEW: Chat interface component with message history display and input field. Implement chat-based user interface on the frontend alongside existing task management UI.

### Code Quality and Conventions
Type-safe everywhere (TS in frontend, Pydantic/SQLModel in backend). Clean, readable code: Follow CLAUDE.md guidelines in root/frontend/backend. Error handling: Graceful, informative. Environment variables only for secrets/config. Docker-compose for local dev. Clear separation between AI logic and database operations. Maintain clean, readable, and maintainable code with incremental enhancements.

### Workflow and Iteration
Use Spec-Kit phases: Current is phase3-chatbot extending phase2-web. Update specs on requirement changes. Test locally: Frontend `npm run dev`, Backend `uvicorn main:app --reload`. Commit often with clear messages. Preserve Phase 2 functionality while adding Phase 3 features.

### Interactive Chatbot Requirements
Chatbot must be fully functional with no disabled inputs or broken forms. User MUST be able to type messages, Submit button MUST be clickable, Messages MUST be sent to backend, AI response MUST render in UI. All UI components must be tested for interaction. Chat functionality: User types message → clicks submit → Message is sent to POST /api/{user_id}/chat → Message is saved to database → AI agent processes message → MCP tools are invoked when needed (add_task, list_tasks, update_task, complete_task).

### Floating Chatbot UI Design
Implement a floating chatbot icon/button that is visible on all authenticated pages with fixed position (bottom-right recommended). Clicking the icon MUST open the chatbot panel, and clicking close/minimize MUST hide the chatbot panel. Chatbot panel opens as a modal or slide-up panel containing: Header (e.g. "Todo AI Assistant"), Scrollable message area, Message input field, Submit / Send button. Input field MUST be enabled and focusable, Submit button MUST trigger message send.

### Real-Time Interaction Design
UI/UX must be professional with clear distinction between user and assistant messages. Smooth open/close animation required. Auto-scroll to latest message. Optional typing indicator ("Assistant is typing..."). Professional styling using Tailwind CSS. Ensure chatbot is interactive and usable by real users with proper feedback mechanisms.

### AI Integration Principles
Integrate OpenAI Agents SDK for natural language understanding in the chatbot. AI responses must be aligned with the task management context only. The chatbot should only act on user-authorized data. No cross-user data access is allowed. Reuse existing authentication, database, and task APIs for AI operations. Implement MCP tools integration for task operations (add, list, update, complete, delete) through natural language processing.

### MCP Tools Integration
Use MCP tools for task operations triggered by natural language commands. Implement standardized interfaces for add, list, update, complete, delete operations accessible via AI agent. Ensure all MCP operations respect user authentication and data isolation. Operations must correctly reflect task changes in the database and return accurate responses to the user.

### Chat Interface Design
Implement intuitive chat-based user interface that allows users to manage tasks using natural language conversation. Display conversation history with clear distinction between user and bot messages. Provide feedback mechanisms for successful and failed operations. Ensure the chat interface integrates seamlessly with existing task management UI.

### Data Privacy and Ethics
The chatbot should only act on user-authorized data. No cross-user data access is allowed. AI responses must be aligned with the task management context only. Ensure user data isolation and security. Implement proper logging and audit trails for AI operations. Protect sensitive user information in chat history.

## Security Requirements
All endpoints must enforce authentication and authorization. Data isolation between users is mandatory. Use environment variables for secrets. Implement proper error handling without exposing internal details to clients. Follow OWASP security guidelines for web applications. Ensure secure handling of AI-generated content and chat history. Protect against prompt injection and other AI-specific security threats.

## Development Workflow
All code changes must start with an update to the relevant specification document in `/specs/`. Use feature branches for development. Implement test-driven development where appropriate. Code reviews are mandatory for all pull requests. Maintain backward compatibility when possible and use proper versioning for breaking changes. Incremental enhancement of the Phase 2 system while preserving existing functionality.

## Governance
This constitution defines non-negotiable rules, principles, and standards that ALL generated specifications, plans, tasks, and code MUST strictly follow. It ensures consistency, security, quality, and alignment with the project requirements. Any changes to this constitution require explicit approval and must be documented with a clear rationale. Build Phase 3 within the existing Phase 2 codebase, reusing existing authentication, database, and task APIs.

**Version**: 1.3.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-31