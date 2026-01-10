---
description: "Task list for Hackathon II Todo full-stack web application with authentication and task CRUD"
---

# Tasks: Hackathon II Todo – Phase II: Full-Stack Web Application

**Input**: Design documents from `/specs/001-phase2-web/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are the actual implementation tasks for the Hackathon II Todo app
  based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks are organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with backend and frontend directories per implementation plan
- [X] T002 [P] Initialize backend with FastAPI dependencies in backend/requirements.txt
- [X] T003 [P] Initialize frontend with Next.js dependencies in frontend/package.json
- [X] T004 [P] Configure basic docker-compose.yml with PostgreSQL service
- [X] T005 Setup environment variables and .env example files for both backend and frontend

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Create SQLModel Task model with user_id foreign key in backend/models/task.py
- [X] T007 Create database session and connection setup in backend/database/session.py
- [ ] T008 [P] Configure Better Auth in frontend with JWT plugin and shared secret
- [X] T009 [P] Create JWT verification middleware in backend/middleware/auth.py
- [X] T010 Create dependency to get current authenticated user in backend/api/deps.py
- [X] T011 Create centralized API client with automatic JWT attachment in frontend/src/lib/api.ts
- [X] T012 Setup automatic table creation strategy for hackathon in backend/database/session.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---
## Phase 3: User Story 1 - User Authentication (Signup/Login) (Priority: P1) 🎯 MVP

**Goal**: New users can sign up for an account and existing users can log in to access their tasks. This enables the multi-user functionality that is fundamental to the application.

**Independent Test**: A new user can complete the signup process with valid credentials and then log in to the application, gaining access to a personal dashboard where they can create and manage tasks.

### Implementation for User Story 1

- [X] T013 Create Login page component in frontend/src/app/login/page.tsx
- [X] T014 Create Signup page component in frontend/src/app/signup/page.tsx
- [X] T015 Create protected layout component in frontend/src/app/layout.tsx
- [X] T016 Create authentication state management using Better Auth hooks in frontend/src/lib/auth.ts
- [X] T017 Implement route guarding to redirect unauthenticated users in frontend/src/components/ProtectedRoute.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---
## Phase 4: User Story 2 - Task CRUD Operations (Priority: P1)

**Goal**: Authenticated users can create, read, update, and delete their personal tasks. This implements the core functionality of a todo application.

**Independent Test**: A logged-in user can create a new task, view their list of tasks, edit an existing task, mark tasks as completed, and delete tasks, with all changes persisting across sessions.

### Implementation for User Story 2

- [ ] T018 [P] [US2] Implement GET /api/tasks endpoint with filtering and sorting in backend/api/routes/tasks.py
- [ ] T019 [P] [US2] Implement POST /api/tasks endpoint in backend/api/routes/tasks.py
- [ ] T020 [P] [US2] Implement GET /api/tasks/{id} endpoint in backend/api/routes/tasks.py
- [ ] T021 [US2] Implement PUT /api/tasks/{id} endpoint in backend/api/routes/tasks.py
- [ ] T022 [US2] Implement DELETE /api/tasks/{id} endpoint in backend/api/routes/tasks.py
- [X] T023 [US2] Create Dashboard page with task list in frontend/src/app/dashboard/page.tsx
- [X] T024 [US2] Create TaskList component to display user's tasks in frontend/src/components/TaskList.tsx
- [X] T025 [US2] Create TaskCard component for individual task display in frontend/src/components/TaskCard.tsx
- [X] T026 [US2] Create CreateTaskForm component in frontend/src/components/CreateTaskForm.tsx
- [X] T027 [US2] Integrate API client with task creation in frontend/src/components/CreateTaskForm.tsx
- [X] T028 [US2] Implement task display with details in frontend/src/components/TaskList.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---
## Phase 5: User Story 4 - Task Completion Toggle (Priority: P1)

**Goal**: Users can easily mark tasks as completed or pending with a single action, providing quick status updates for their tasks.

**Independent Test**: A logged-in user can mark a task as completed by clicking a checkbox or button, and the task's status updates immediately in the interface and is persisted in the database.

### Implementation for User Story 4

- [X] T029 [P] [US4] Implement PATCH /api/tasks/{id}/complete endpoint in backend/api/routes/tasks.py
- [X] T030 [US4] Add completion toggle functionality to TaskCard component in frontend/src/components/TaskCard.tsx
- [X] T031 [US4] Create API function for toggling task completion in frontend/src/lib/api.ts
- [X] T032 [US4] Update task status in UI immediately after API call in frontend/src/components/TaskCard.tsx

**Checkpoint**: At this point, User Stories 1, 2, and 4 should all work independently

---
## Phase 6: User Story 3 - Task Filtering and Sorting (Priority: P2)

**Goal**: Authenticated users can filter their tasks by completion status and sort them by creation date or title, making it easier to manage large task lists.

**Independent Test**: A logged-in user can apply filters to see only pending or completed tasks, and can sort their tasks by creation date or title in ascending or descending order.

### Implementation for User Story 3

- [X] T033 [P] [US3] Create TaskFilter component for filtering by status in frontend/src/components/TaskFilter.tsx
- [X] T034 [US3] Add sorting functionality to TaskList component in frontend/src/components/TaskList.tsx
- [X] T035 [US3] Update API client to support filtering and sorting parameters in frontend/src/lib/api.ts
- [X] T036 [US3] Enhance GET /api/tasks endpoint with proper query parameter handling in backend/api/routes/tasks.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T037 [P] Add responsive design with Tailwind CSS to all components
- [ ] T038 [P] Add proper error handling and user feedback messages
- [ ] T039 Add loading states and UI feedback for API calls
- [ ] T040 Add proper data validation and error checking
- [ ] T041 [P] Add environment configuration for different deployment stages
- [ ] T042 Add proper logging and error tracking
- [ ] T043 Add automated tests for backend API endpoints
- [ ] T044 Add automated tests for frontend components
- [ ] T045 Run quickstart.md validation and update as needed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 4 (P1)**: Can start after Foundational (Phase 2) - Builds on US2 task display
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Builds on US2 task display

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in priority order
- All models within a story marked [P] can run in parallel
- Different user stories can be worked on in priority order

---

## Implementation Strategy

### MVP First (User Stories 1 and 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 2 (Basic CRUD)
5. **STOP and VALIDATE**: Test authentication and basic task management independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (Authentication!)
3. Add User Story 2 → Test independently → Deploy/Demo (CRUD!)
4. Add User Story 4 → Test independently → Deploy/Demo (Completion toggle!)
5. Add User Story 3 → Test independently → Deploy/Demo (Filtering/Sorting!)
6. Each story adds value without breaking previous stories

### Success Criteria for Each Task

- T001: Project directories (backend/, frontend/) exist and are properly structured
- T002-T003: Dependencies are properly defined in requirements.txt and package.json
- T004: Docker Compose file exists and defines PostgreSQL service
- T005: Environment files exist with proper variable definitions
- T006: Task model exists with proper fields and relationships per data-model.md
- T007: Database session management is properly configured
- T008: Better Auth is configured with JWT plugin in frontend
- T009: JWT middleware exists and verifies tokens properly
- T010: Current user dependency function exists and extracts user_id from token
- T011: API client exists and automatically attaches JWT to requests
- T012: Table creation strategy is implemented
- T013-T016: Authentication pages exist and function properly
- T018-T022: All CRUD endpoints exist and function per API contracts
- T023-T028: Task management UI exists and integrates with API
- T029-T032: Task completion toggle works in both frontend and backend
- T033-T036: Filtering and sorting functionality works as specified