# Implementation Plan: Hackathon II Todo – Phase II: Full-Stack Web Application

**Branch**: `001-phase2-web` | **Date**: 2026-01-02 | **Spec**: [specs/001-phase2-web/spec.md](specs/001-phase2-web/spec.md)
**Input**: Feature specification from `/specs/001-phase2-web/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a secure, multi-user full-stack Todo web application with persistent storage. The solution will integrate Better Auth for JWT-based authentication with a FastAPI backend, enforce strict data isolation, implement full Task CRUD operations with filtering/sorting capabilities, and create a responsive Next.js frontend with App Router. The architecture follows a stateless authentication pattern with JWT tokens for secure API communication. This plan includes detailed technical architecture, component breakdown, authentication integration, database setup, API implementation order, frontend implementation order, and local development guidelines.

## Technical Context

**Language/Version**: Python 3.11+ (Backend), TypeScript 5.0+ (Frontend), Node.js 18+
**Primary Dependencies**: FastAPI, SQLModel, Better Auth, Next.js 16+, Tailwind CSS
**Storage**: Neon Serverless PostgreSQL with SQLModel ORM
**Testing**: pytest (Backend), Jest/React Testing Library (Frontend)
**Target Platform**: Web application (Responsive)
**Project Type**: Web (separate frontend/backend)
**Performance Goals**: <2 second load for task lists (up to 100 tasks), <10 second task creation, 95% successful login rate
**Constraints**: JWT token expiry within 7 days, data isolation between users, mobile-responsive UI
**Scale/Scope**: Support 1000+ concurrent users, individual user task limits not specified

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Spec-Driven Development: Following feature spec from `/specs/001-phase2-web/spec.md`
- ✅ Monorepo Structure: Will create `/frontend/` and `/backend/` directories as required
- ✅ Technology Stack Compliance: Using Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth with JWT
- ✅ Security and Authentication: All endpoints will require JWT authentication, data isolation enforced
- ✅ API Design: Will implement stateless endpoints as specified (no user_id in path)
- ✅ Database Rules: Using SQLModel with proper user_id foreign keys and indexing
- ✅ Frontend Patterns: Creating API client in `/lib/api.ts` with JWT attachment
- ✅ Code Quality: Type-safe with TypeScript/Pydantic, proper error handling

## Project Structure

### Documentation (this feature)
```text
specs/001-phase2-web/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command output)
├── data-model.md        # Phase 1 output (/sp.plan command output)
├── quickstart.md        # Phase 1 output (/sp.plan command output)
├── contracts/           # Phase 1 output (/sp.plan command output)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
backend/
├── main.py
├── models/
│   ├── __init__.py
│   └── task.py
├── database/
│   ├── __init__.py
│   └── session.py
├── api/
│   ├── __init__.py
│   ├── deps.py
│   └── routes/
│       ├── __init__.py
│       └── tasks.py
├── middleware/
│   ├── __init__.py
│   └── auth.py
└── requirements.txt

frontend/
├── package.json
├── next.config.js
├── tailwind.config.js
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── signup/
│   │   │   └── page.tsx
│   │   └── dashboard/
│   │       └── page.tsx
│   ├── components/
│   │   ├── TaskList.tsx
│   │   ├── TaskCard.tsx
│   │   ├── CreateTaskForm.tsx
│   │   └── TaskFilter.tsx
│   ├── lib/
│   │   └── api.ts
│   └── types/
│       └── index.ts
├── styles/
│   └── globals.css
└── tsconfig.json
```

**Structure Decision**: Selected Option 2: Web application with separate frontend (Next.js) and backend (FastAPI) to maintain clear separation of concerns and allow independent scaling/deployment.

## Detailed Architecture Plan

### 1. High-Level Architecture Diagram Description
Flow: User → Frontend (Next.js + Better Auth) → JWT issuance → API calls with Bearer token → FastAPI backend → JWT verification middleware → SQLModel queries (filtered by user_id) → Neon PostgreSQL.

### 2. Component Breakdown

#### Frontend Components and Pages:
- **Layout Component**: Common layout with navigation
- **LoginPage**: Authentication form with email/password
- **SignupPage**: Registration form with email/password
- **DashboardPage**: Main task management interface
- **TaskList**: Displays user's tasks with filtering/sorting capabilities
- **TaskCard**: Individual task display with completion toggle
- **CreateTaskForm**: Form for creating new tasks
- **TaskFilter**: UI controls for filtering by status and sorting

#### Backend Modules:
- **main.py**: FastAPI application entry point with CORS and middleware setup
- **models/task.py**: SQLModel definition for Task entity with user_id foreign key
- **database/session.py**: Database session management with engine setup
- **api/routes/tasks.py**: Task-related API endpoints (CRUD operations)
- **middleware/auth.py**: JWT verification middleware and current_user dependency
- **api/deps.py**: Dependency injection utilities for authentication and database sessions

### 3. Authentication Integration Plan

#### Better Auth Configuration:
- Enable JWT plugin in Better Auth
- Use shared BETTER_AUTH_SECRET environment variable for signing/verification
- Configure user session management in Next.js frontend

#### Frontend Implementation:
- Session management with automatic JWT attachment in API client
- Create centralized API client in `/lib/api.ts` that automatically attaches JWT tokens
- Implement authentication state management using Better Auth hooks

#### Backend Implementation:
- JWT verification middleware using PyJWT
- Dependency function to extract current_user_id from token
- Protected routes enforcement with proper 401 responses

### 4. Database Setup Plan

#### SQLModel Models:
- Task model with user_id foreign key for data isolation
- Proper indexing on user_id and completed fields for performance
- Automatic validation and serialization

#### Session Management:
- Database session dependency injection
- Proper connection handling and resource cleanup
- Automatic table creation for hackathon (or migration strategy)

### 5. API Implementation Order

1. **JWT middleware**: Implement authentication middleware before any task routes
2. **GET /api/tasks**: List tasks endpoint with filtering/sorting (user_id isolation)
3. **POST /api/tasks**: Create task endpoint (associate with current user)
4. **GET /api/tasks/{id}**: Get single task endpoint (verify user ownership)
5. **PUT /api/tasks/{id}**: Update task endpoint (verify user ownership)
6. **DELETE /api/tasks/{id}**: Delete task endpoint (verify user ownership)
7. **PATCH /api/tasks/{id}/complete**: Toggle completion endpoint (verify user ownership)

### 6. Frontend Implementation Order

1. **API client**: Create centralized API client in `/lib/api.ts` with JWT attachment
2. **Authentication pages**: Login and Signup pages with Better Auth integration
3. **Dashboard layout**: Basic dashboard structure with navigation
4. **TaskList component**: Display tasks with basic styling
5. **TaskCard component**: Individual task display with completion toggle
6. **CreateTaskForm component**: Form for creating new tasks
7. **TaskFilter component**: Filtering and sorting functionality
8. **Integration**: Connect all components with API client

### 7. Step-by-Step Implementation Tasks

- Complete JWT middleware before implementing any task routes
- Set up database models before creating API endpoints
- Implement authentication before creating task management features
- Create API client before building frontend components
- Test authentication flow before implementing task CRUD
- Verify data isolation between users before completing implementation

### 8. Local Development & Testing Plan

#### Docker Compose Setup:
- PostgreSQL service for local development
- Separate services for frontend and backend development servers

#### Running Both Services:
- Backend: `uvicorn main:app --reload` for development
- Frontend: `npm run dev` for development

#### Manual Testing Flow:
- Signup with new account
- Login to application
- Create task and verify it appears in list
- Update task and verify changes persist
- Mark task as complete and verify status change
- Delete task and verify removal
- Verify only current user's tasks are visible

### 9. Potential Risks & Mitigations

#### Common Issues with Better Auth + FastAPI JWT Integration:
- Token format mismatches: Ensure both services use compatible JWT formats
- Secret key synchronization: Use shared BETTER_AUTH_SECRET environment variable
- Token expiry handling: Implement proper refresh mechanisms if needed

#### Token Handling Edge Cases:
- Expired tokens: Redirect to login or attempt refresh
- Invalid tokens: Handle gracefully with appropriate error messages
- Network failures: Implement retry logic and proper error handling

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None] | [No violations identified] | [All constitution requirements satisfied] |