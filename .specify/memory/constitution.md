<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles:
- Added 9 core principles specific to the Hackathon II Todo app
Added sections: Security and Authentication, API Design, Database Rules, Frontend Patterns, Code Quality and Conventions, Workflow and Iteration
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->
# Hackathon II Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-Driven Development
Every change starts with updating or referencing specs in `/specs/`. Use `@specs/path/to/file.md` for references. Specs are organized by type: features, api, database, ui. Never implement without a spec.

### Monorepo Structure
Maintain the exact folder structure from documentation: `/specs/` with subfolders (features/, api/, database/, ui/), `/frontend/` (Next.js), `/backend/` (FastAPI), Root `CLAUDE.md`, `frontend/CLAUDE.md`, `backend/CLAUDE.md` for guidelines. `.spec-kit/config.yaml` with defined phases (phase2-web includes task-crud and authentication).

### Technology Stack Compliance
Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS. Server components default; client components only for interactivity. No inline styles. Backend: Python FastAPI, SQLModel ORM, Neon Serverless PostgreSQL. Auth: Better Auth (frontend) with JWT plugin enabled. Shared `BETTER_AUTH_SECRET` env variable for signing/verification. API: RESTful, JSON responses, Pydantic models.

### Security and Authentication (Mandatory for ALL Endpoints)
Stateless JWT authentication: Frontend issues JWT on login/signup; attach to every API request in `Authorization: Bearer <token>` header. Backend: Middleware to verify JWT signature with shared secret, extract user_id, and enforce on every route. 401 Unauthorized for missing/invalid/expired tokens. Data Isolation: EVERY database query MUST filter by authenticated `user_id` (e.g., `WHERE user_id = current_user_id`). No cross-user data access. Token Expiry: Default 7 days; configurable but always enforce expiry. Users table managed by Better Auth; tasks have `user_id` foreign key.

### API Design
Updated endpoints (stateless, no {user_id} in path): GET /api/tasks (list with filters: status, sort), POST /api/tasks, GET /api/tasks/{id}, PUT /api/tasks/{id}, DELETE /api/tasks/{id}, PATCH /api/tasks/{id}/complete (toggle). Use proper HTTP methods, status codes, error handling (HTTPException). Filter responses to authenticated user's tasks only.

### Database Rules
Schema exactly as in `/specs/database/schema.md`: users (Better Auth), tasks (id, user_id FK, title, description, completed, timestamps). Indexes on user_id and completed. Use SQLModel for models, queries, sessions. Connection via `DATABASE_URL` env.

### Frontend Patterns
API client in `/lib/api.ts`: Attach JWT to all requests. Responsive UI with Tailwind. Pages: Login/Signup, Task list (filter/sort), Create/Edit forms.

### Code Quality and Conventions
Type-safe everywhere (TS in frontend, Pydantic/SQLModel in backend). Clean, readable code: Follow CLAUDE.md guidelines in root/frontend/backend. Error handling: Graceful, informative. Environment variables only for secrets/config. Docker-compose for local dev.

### Workflow and Iteration
Use Spec-Kit phases: Current is phase2-web. Update specs on requirement changes. Test locally: Frontend `npm run dev`, Backend `uvicorn main:app --reload`. Commit often with clear messages.

## Security Requirements
All endpoints must enforce authentication and authorization. Data isolation between users is mandatory. Use environment variables for secrets. Implement proper error handling without exposing internal details to clients. Follow OWASP security guidelines for web applications.

## Development Workflow
All code changes must start with an update to the relevant specification document in `/specs/`. Use feature branches for development. Implement test-driven development where appropriate. Code reviews are mandatory for all pull requests. Maintain backward compatibility when possible and use proper versioning for breaking changes.

## Governance
This constitution defines non-negotiable rules, principles, and standards that ALL generated specifications, plans, tasks, and code MUST strictly follow. It ensures consistency, security, quality, and alignment with the project requirements. Any changes to this constitution require explicit approval and must be documented with a clear rationale.

**Version**: 1.1.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-02