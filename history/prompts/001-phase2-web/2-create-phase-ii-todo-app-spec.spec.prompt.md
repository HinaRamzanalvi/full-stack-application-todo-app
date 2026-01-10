---
id: 2
title: Create Phase II Todo App Spec
stage: spec
date: 2026-01-02
surface: agent
model: Claude Sonnet 4.5
feature: 001-phase2-web
branch: 001-phase2-web
user: Admin
command: /sp.specify
labels: [spec, todo-app, fullstack, authentication, crud]
links:
  spec: specs/001-phase2-web/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-phase2-web/spec.md
  - specs/001-phase2-web/checklists/requirements.md
tests:
  - none
---

## Prompt

Generate a complete, detailed, and structured specification for Phase II of the Hackathon Todo application using the Spec-Kit Plus conventions and the existing project structure.

Project: Hackathon II Todo – Phase II: Full-Stack Web Application (Basic Level Functionality)

Objective: Transform the existing console Todo app into a modern multi-user web application with persistent storage, user authentication, and full Task CRUD operations.

Current Phase: phase2-web (includes features: task-crud and authentication)

Strictly follow the constitution already defined in memory.

Key Requirements from Documentation:
- Implement all 5 Basic Level features as a web application:
  1. Create new tasks
  2. List all tasks with filtering/sorting
  3. View task details
  4. Update tasks
  5. Delete tasks + Toggle completion
- Multi-user support: Each user sees and modifies only their own tasks
- Persistent storage in Neon Serverless PostgreSQL
- Authentication: User signup and signin using Better Auth
- Secure REST API with stateless JWT authentication (shared BETTER_AUTH_SECRET)
- Responsive frontend interface

Technology Stack (must be followed exactly):
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (configured with JWT plugin)

API Endpoints (Stateless – no {user_id} in path):
- GET /api/tasks              → List tasks (query params: status=all/pending/completed, sort=created/title)
- POST /api/tasks             → Create task
- GET /api/tasks/{id}         → Get single task
- PUT /api/tasks/{id}         → Update task
- DELETE /api/tasks/{id}      → Delete task
- PATCH /api/tasks/{id}/complete → Toggle completion

Security Rules:
- All endpoints require valid JWT in Authorization: Bearer <token> header
- Backend verifies JWT and extracts user_id
- Every database operation MUST filter by authenticated user_id
- 401 Unauthorized on missing/invalid token

Database Schema:
- users table: managed by Better Auth (id, email, name, etc.)
- tasks table: id, user_id (FK → users.id), title (required), description (optional), completed (bool, default false), created_at, updated_at
- Indexes: on tasks.user_id and tasks.completed

Frontend Requirements:
- Pages: Login/Signup, Dashboard with task list, Create/Edit task forms
- Use server components by default
- API calls via centralized client that attaches JWT automatically
- Responsive design with Tailwind CSS

Organize the generated specification into the existing /specs/ structure:
- Update/Add to /specs/overview.md (project status, current phase)
- /specs/features/task-crud.md (detailed user stories and acceptance criteria)

## Response snapshot

Created a comprehensive specification for the Hackathon II Todo application Phase II. The specification includes:

- User Stories for authentication, task CRUD operations, filtering/sorting, and task completion toggle
- Functional requirements covering all necessary features
- Key entities (User and Task)
- Success criteria with measurable outcomes
- Edge cases handling

The specification follows the template structure and includes 4 prioritized user stories with acceptance scenarios. All requirements are testable and technology-agnostic as required by the constitution.

## Outcome

- ✅ Impact: Created complete spec for full-stack todo app with authentication and CRUD
- 🧪 Tests: No tests required for specification creation
- 📁 Files: Created specs/001-phase2-web/spec.md and checklists/requirements.md
- 🔁 Next prompts: Ready to proceed with planning phase
- 🧠 Reflection: Specification covers all required features with clear acceptance criteria

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All requirements met
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase with /sp.plan