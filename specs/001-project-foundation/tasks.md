---
description: "Task list for project foundation and architecture implementation"
---

# Tasks: Project Foundation & Architecture

**Input**: Design documents from `/specs/001-project-foundation/`
**Prerequisites**: plan.md (completed), spec.md (completed), research.md (completed), data-model.md (completed), contracts/ (completed)

**Tests**: No tests requested in specification. Tasks focus on configuration, documentation, and directory structure.

**Organization**: Tasks are grouped by user story to enable independent implementation and validation of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

This is a web application monorepo:
- **Frontend**: `frontend/` (Next.js 16+ application)
- **Backend**: `backend/` (FastAPI application)
- **Specs**: `specs/` (Spec-Kit Plus documentation)
- **Configuration**: Root-level files (docker-compose.yml, .gitignore, README.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic monorepo structure

- [X] T001 Create frontend/ directory with Next.js 16 structure (app/, components/, lib/, public/)
- [X] T002 [P] Create backend/ directory with FastAPI structure (routes/, middleware/, schemas/, services/)
- [X] T003 [P] Create specs/ subdirectories (features/, api/, database/, ui/) per FR-013
- [X] T004 [P] Initialize root .gitignore with Node.js and Python patterns per research.md decision

**Checkpoint**: ✅ Basic directory structure established

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create root .env.example documenting all shared environment variables (BETTER_AUTH_SECRET, NODE_ENV)
- [X] T006 Update root CLAUDE.md with project navigation, Spec-Driven Development workflow, API endpoints reference, and authentication overview

**Checkpoint**: ✅ Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Developer Sets Up Project Structure (Priority: P1) 🎯 MVP

**Goal**: Enable developers to understand complete project structure and navigate monorepo layout with all directories and initial configuration files in place

**Independent Test**: Clone repository, navigate through directories, verify frontend/, backend/, specs/, history/, .specify/ exist with proper subdirectories. Open root CLAUDE.md and verify navigation links work.

**Acceptance Criteria**:
- Frontend/, backend/, specs/, history/, .specify/ directories visible at root (FR-001)
- Root CLAUDE.md provides navigation to component instructions (FR-002)
- Specs/ contains features/, api/, database/, ui/ subdirectories (FR-013)

### Implementation for User Story 1

- [X] T007 [P] [US1] Create frontend/app/ directory structure with (auth)/, (dashboard)/, api/ route groups
- [X] T008 [P] [US1] Create frontend/components/ directory with ui/ and features/ subdirectories
- [X] T009 [P] [US1] Create frontend/lib/ directory for utilities (auth.ts, api-client.ts, utils.ts planned)
- [X] T010 [P] [US1] Create frontend/public/ directory for static assets
- [X] T011 [P] [US1] Create backend/routes/ directory with __init__.py placeholder
- [X] T012 [P] [US1] Create backend/middleware/ directory with __init__.py placeholder
- [X] T013 [P] [US1] Create backend/schemas/ directory with __init__.py placeholder
- [X] T014 [P] [US1] Create backend/services/ directory with __init__.py placeholder
- [X] T015 [P] [US1] Create empty specs/features/ directory (populated by future features)
- [X] T016 [P] [US1] Create empty specs/api/ directory (populated when API designed)
- [X] T017 [P] [US1] Create empty specs/database/ directory (populated when models designed)
- [X] T018 [P] [US1] Create empty specs/ui/ directory (populated when UI designed)

**Checkpoint**: ✅ All directories created - Developer can navigate project structure (User Story 1 complete)

---

## Phase 4: User Story 2 - Developer Configures Local Environment (Priority: P1)

**Goal**: Enable developers to configure local development environment with proper environment variables, understanding what each variable does and critical matching requirements for BETTER_AUTH_SECRET

**Independent Test**: Navigate to frontend/ and backend/ directories, find .env.example templates. Read variable descriptions and verify BETTER_AUTH_SECRET matching requirement is documented. Verify port configuration (3000, 8000) is clear.

**Acceptance Criteria**:
- Frontend/.env.example and backend/.env.example exist with all variables documented (FR-005)
- BETTER_AUTH_SECRET matching requirement explicitly stated (FR-006)
- Port configuration clear (Frontend 3000, Backend 8000) (FR-008)

### Implementation for User Story 2

- [X] T019 [US2] Create frontend/.env.example with BETTER_AUTH_SECRET, NEXT_PUBLIC_API_URL, NODE_ENV (include descriptions per data-model.md)
- [X] T020 [US2] Create backend/.env.example with BETTER_AUTH_SECRET, DATABASE_URL, CORS_ORIGINS, PORT (include descriptions per data-model.md)
- [X] T021 [US2] Add comment in both .env.example files warning that BETTER_AUTH_SECRET must match between frontend and backend (FR-006 critical requirement)
- [X] T022 [US2] Document in frontend/.env.example that NEXT_PUBLIC_API_URL should be http://localhost:8000
- [X] T023 [US2] Document in backend/.env.example that CORS_ORIGINS should be http://localhost:3000
- [X] T024 [US2] Add validation note in frontend/.env.example that BETTER_AUTH_SECRET minimum length is 32 characters
- [X] T025 [US2] Add note in both .env.example files referencing root .env.example as source of truth per research.md decision

**Checkpoint**: ✅ Environment configuration templates complete - Developer can configure services (User Story 2 complete)

---

## Phase 5: User Story 3 - Developer Understands System Architecture (Priority: P1)

**Goal**: Enable developers and architects to understand complete system architecture including component interactions, JWT authentication flow, and user data isolation strategy

**Independent Test**: Read specs/architecture.md and verify all major components (Next.js, FastAPI, PostgreSQL, Better Auth) are documented with clear diagrams. Verify JWT flow shows complete cycle from login to verification. Verify user isolation strategy explains user_id filtering.

**Acceptance Criteria**:
- specs/architecture.md documents system architecture and data flow (FR-009)
- JWT authentication flow documented from login to verification (FR-010)
- User data isolation strategy explains user_id filtering (FR-011)
- specs/overview.md documents project objectives and tech stack (FR-012)

### Implementation for User Story 3

- [X] T026 [P] [US3] Create specs/overview.md documenting project objectives, 5 core CRUD features, tech stack (Next.js 16, FastAPI, SQLModel, Neon PostgreSQL, Better Auth), and authentication approach (JWT with httpOnly cookies)
- [X] T027 [P] [US3] Create specs/architecture.md with system architecture section (multi-tier: Frontend → Backend → Database) referencing contracts/architecture-diagram.md
- [X] T028 [US3] Add JWT authentication flow section to specs/architecture.md referencing contracts/jwt-flow.md with summary of token creation, transmission, and verification
- [X] T029 [US3] Add user data isolation section to specs/architecture.md explaining user_id extraction from JWT and WHERE clause filtering on all database queries
- [X] T030 [US3] Add component interaction section to specs/architecture.md showing request/response cycle from user action to database
- [X] T031 [US3] Add security boundaries section to specs/architecture.md covering httpOnly cookies, CORS, TLS, and user isolation enforcement
- [X] T032 [US3] Add port configuration section to specs/architecture.md documenting Frontend 3000, Backend 8000
- [X] T033 [US3] Add environment variable flow diagram to specs/architecture.md showing root .env → Docker Compose → services with BETTER_AUTH_SECRET consistency

**Checkpoint**: ✅ Architecture documentation complete - Developer understands system design (User Story 3 complete)

---

## Phase 6: User Story 4 - Developer Starts All Services (Priority: P2)

**Goal**: Enable developers to start frontend, backend, and database services simultaneously with a single Docker Compose command

**Independent Test**: Run docker-compose up and verify all services start without errors. Access http://localhost:3000 (frontend) and http://localhost:8000/docs (backend API docs). Run docker-compose down and verify graceful shutdown.

**Acceptance Criteria**:
- Docker Compose configuration starts frontend, backend (FR-007)
- Frontend runs on port 3000, backend on port 8000 (FR-008)
- Services accessible at configured ports
- Graceful shutdown with docker-compose down

### Implementation for User Story 4

- [X] T034 [US4] Create docker-compose.yml with frontend service definition (build: ./frontend, ports: 3000:3000, volumes for hot reload)
- [X] T035 [US4] Add backend service definition to docker-compose.yml (build: ./backend, ports: 8000:8000, volumes for hot reload)
- [X] T036 [US4] Configure environment variable passing in docker-compose.yml (frontend receives BETTER_AUTH_SECRET, NEXT_PUBLIC_API_URL from root .env)
- [X] T037 [US4] Configure environment variable passing for backend in docker-compose.yml (receives BETTER_AUTH_SECRET, DATABASE_URL, CORS_ORIGINS from root .env)
- [X] T038 [US4] Create frontend/Dockerfile with Node.js 18+ base image, npm install, and next dev command
- [X] T039 [US4] Create backend/Dockerfile with Python 3.9+ base image, pip install, and uvicorn reload command
- [X] T040 [US4] Add volume mounts to docker-compose.yml for frontend (./frontend:/app, /app/node_modules) to enable hot reload
- [X] T041 [US4] Add volume mount to docker-compose.yml for backend (./backend:/app) to enable hot reload
- [X] T042 [US4] Add note to docker-compose.yml referencing external Neon PostgreSQL (no local database service per research.md decision)

**Checkpoint**: ✅ Docker orchestration complete - Developer can start all services (User Story 4 complete)

---

## Phase 7: User Story 5 - New Team Member Onboards (Priority: P2)

**Goal**: Enable new developers to understand project, set up environment, and start contributing by following README.md instructions alone

**Independent Test**: Have developer unfamiliar with project follow only README.md to clone, configure, start services, and understand contribution workflow.

**Acceptance Criteria**:
- README.md explains project is multi-user todo app with JWT authentication (FR-014)
- Step-by-step setup instructions allow independent setup (FR-015)
- Development guidelines explain Spec-Driven Development workflow
- Troubleshooting section covers common setup problems

### Implementation for User Story 5

- [X] T043 [US5] Create README.md with project description (multi-user todo app, JWT authentication, 5 core CRUD operations)
- [X] T044 [US5] Add tech stack section to README.md (Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth)
- [X] T045 [US5] Add prerequisites section to README.md (Docker & Docker Compose, Git, Neon PostgreSQL account)
- [X] T046 [US5] Add quick start section to README.md with numbered steps (clone, copy .env.example, configure .env, get Neon DB, docker-compose up)
- [X] T047 [US5] Add environment variables section to README.md documenting all required variables with where to obtain values
- [X] T048 [US5] Add BETTER_AUTH_SECRET matching warning to README.md (must be identical in frontend and backend - critical requirement)
- [X] T049 [US5] Add project structure section to README.md showing directory tree and purposes
- [X] T050 [US5] Add development workflow section to README.md explaining Spec-Driven Development phases (specify, plan, tasks, implement)
- [X] T051 [US5] Add common commands section to README.md (start services, stop services, view logs, access shells, install dependencies)
- [X] T052 [US5] Add troubleshooting section to README.md covering port conflicts, environment variable errors, BETTER_AUTH_SECRET mismatch, database connection issues, Docker not installed
- [X] T053 [US5] Add architecture reference to README.md pointing to specs/architecture.md for detailed system design
- [X] T054 [US5] Add contributing guidelines to README.md (Git workflow, branch naming, commit conventions, PHR creation)

**Checkpoint**: ✅ Onboarding documentation complete - New developer can independently set up and contribute (User Story 5 complete)

---

## Phase 8: User Story 6 - Agent Receives Component-Specific Guidance (Priority: P3)

**Goal**: Provide AI agents and developers with layer-specific instructions unique to frontend (Next.js 16) and backend (FastAPI) without duplicating root-level guidance

**Independent Test**: Read frontend/CLAUDE.md and verify Next.js 16 patterns, Better Auth integration, and frontend architecture are documented. Read backend/CLAUDE.md and verify FastAPI patterns, JWT verification, and user isolation enforcement are documented. Verify both reference root CLAUDE.md for workflow.

**Acceptance Criteria**:
- Frontend CLAUDE.md contains Next.js 16+ guidelines and Better Auth integration (FR-003)
- Backend CLAUDE.md contains FastAPI patterns, SQLModel ORM, JWT verification, user isolation (FR-004)
- Both reference root CLAUDE.md for project-wide policies
- Code examples provided for critical patterns
- Next.js 16 breaking changes documented (FR-016)
- CORS configuration requirements documented (FR-017)
- httpOnly cookie strategy documented (FR-018)

### Implementation for User Story 6

- [X] T055 [P] [US6] Create frontend/CLAUDE.md with Next.js 16 breaking changes section (async params, proxy.ts pattern, server/client components)
- [X] T056 [P] [US6] Add Better Auth integration section to frontend/CLAUDE.md (JWT plugin configuration, httpOnly cookie setup, token storage)
- [X] T057 [P] [US6] Add API proxy pattern section to frontend/CLAUDE.md (how to read httpOnly cookies server-side in /app/api/proxy.ts)
- [X] T058 [P] [US6] Add App Router architecture section to frontend/CLAUDE.md (route groups, dynamic routes, layouts)
- [X] T059 [P] [US6] Add component patterns section to frontend/CLAUDE.md (Server vs Client components, when to use 'use client')
- [X] T060 [P] [US6] Add Tailwind CSS responsive patterns section to frontend/CLAUDE.md (mobile-first, breakpoints, utility classes)
- [X] T061 [P] [US6] Add code standards section to frontend/CLAUDE.md (TypeScript types, naming conventions, file organization)
- [X] T062 [P] [US6] Add reference to root CLAUDE.md in frontend/CLAUDE.md for Spec-Driven Development workflow
- [X] T063 [P] [US6] Create backend/CLAUDE.md with FastAPI application structure section (main.py, routes/, middleware/, models.py organization)
- [X] T064 [P] [US6] Add SQLModel ORM patterns section to backend/CLAUDE.md (model definition, relationships, queries with user filtering)
- [X] T065 [P] [US6] Add JWT verification middleware section to backend/CLAUDE.md (token extraction, signature verification, user attachment to request.state)
- [X] T066 [P] [US6] Add user isolation enforcement section to backend/CLAUDE.md with checklist (extract user_id from JWT, validate URL user_id matches, filter all queries: WHERE user_id = ...)
- [X] T067 [P] [US6] Add database connection section to backend/CLAUDE.md (Neon PostgreSQL setup, DATABASE_URL usage, SQLModel.create_all)
- [X] T068 [P] [US6] Add API endpoint patterns section to backend/CLAUDE.md (RESTful conventions, request/response schemas, error handling)
- [X] T069 [P] [US6] Add security requirements section to backend/CLAUDE.md (no hardcoded secrets, input validation, SQL injection prevention via ORM)
- [X] T070 [P] [US6] Add CORS configuration section to backend/CLAUDE.md (credentials: true for httpOnly cookies, allowed origins)
- [X] T071 [P] [US6] Add code examples to frontend/CLAUDE.md for async params pattern (Next.js 16 correct vs incorrect)
- [X] T072 [P] [US6] Add code examples to backend/CLAUDE.md for user isolation enforcement (route handler with user_id validation)
- [X] T073 [P] [US6] Add reference to root CLAUDE.md in backend/CLAUDE.md for Spec-Driven Development workflow

**Checkpoint**: ✅ Component-specific guidance complete - Agents have layer-specific instructions (User Story 6 complete)

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements and validations that affect multiple user stories

- [X] T074 [P] Add frontend/README.md with local development instructions (npm install, npm run dev)
- [X] T075 [P] Add backend/README.md with local development instructions (pip install, uvicorn main:app --reload)
- [X] T076 [P] Create frontend/.gitignore with Next.js patterns (.next/, node_modules/, .env)
- [X] T077 [P] Create backend/.gitignore with Python patterns (__pycache__/, *.pyc, .env, .pytest_cache/)
- [X] T078 [P] Validate all documentation cross-references (CLAUDE.md files link to specs/, README references architecture)
- [X] T079 [P] Validate BETTER_AUTH_SECRET matching requirement documented in at least 3 locations (root CLAUDE.md, .env.example files, README.md per success criteria SC-010)
- [X] T080 Verify directory structure matches contracts/directory-structure.md specification
- [X] T081 Verify all FR-001 through FR-020 requirements are satisfied
- [X] T082 Run validation: Clone fresh repository, follow README.md setup, verify all files exist and Docker Compose starts successfully

**Checkpoint**: ✅ All polish tasks complete - Project foundation ready for feature implementation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational (Phase 2) completion
  - User Story 1 (P1): Can start after Foundational
  - User Story 2 (P1): Can start after Foundational (independent of US1)
  - User Story 3 (P1): Can start after Foundational (independent of US1, US2)
  - User Story 4 (P2): Can start after Foundational (independent of other stories)
  - User Story 5 (P2): Can start after Foundational (independent of other stories)
  - User Story 6 (P3): Can start after Foundational (independent of other stories)
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

**All user stories are INDEPENDENT** - each can be implemented and tested separately after Foundational phase:

- **User Story 1 (P1)**: Directory structure - No dependencies on other stories
- **User Story 2 (P1)**: Environment configuration - No dependencies on other stories
- **User Story 3 (P1)**: Architecture docs - No dependencies on other stories (references contracts/ already created in planning)
- **User Story 4 (P2)**: Docker Compose - No dependencies on other stories (can start services even without docs)
- **User Story 5 (P2)**: README onboarding - No dependencies on other stories (references other deliverables but can be written independently)
- **User Story 6 (P3)**: Component CLAUDE.md - No dependencies on other stories (references root CLAUDE.md from Foundational)

### Within Each User Story

- **User Story 1**: All directory creation tasks marked [P] can run in parallel
- **User Story 2**: Tasks must run sequentially (create .env.example files before adding comments)
- **User Story 3**: T026, T027 marked [P] can run in parallel, then T028-T033 build on T027
- **User Story 4**: T034-T035 create compose file, T036-T037 add env config, T038-T039 create Dockerfiles [P], T040-T042 add volume config
- **User Story 5**: Tasks must run sequentially (build README.md section by section)
- **User Story 6**: All frontend CLAUDE.md tasks (T055-T062, T071) marked [P], all backend CLAUDE.md tasks (T063-T073) marked [P] - can work on frontend and backend simultaneously

### Parallel Opportunities

**Setup Phase (Phase 1)**:
- T002, T003, T004 can run in parallel

**Foundational Phase (Phase 2)**:
- T005, T006 can run in parallel

**User Story 1 (All parallel)**:
- T007-T018 can all run in parallel (different directories)

**User Story 3 (Partial parallel)**:
- T026, T027 can run in parallel

**User Story 4 (Partial parallel)**:
- T038, T039 can run in parallel (Dockerfiles)

**User Story 6 (High parallel)**:
- Frontend tasks: T055-T062, T071 can all run in parallel
- Backend tasks: T063-T073 can all run in parallel
- Frontend and backend groups can run simultaneously

**Polish Phase (Phase 9)**:
- T074-T079 can all run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all directory creation tasks for User Story 1 together:
Task: "Create frontend/app/ directory structure with (auth)/, (dashboard)/, api/ route groups"
Task: "Create frontend/components/ directory with ui/ and features/ subdirectories"
Task: "Create frontend/lib/ directory for utilities"
Task: "Create frontend/public/ directory for static assets"
Task: "Create backend/routes/ directory with __init__.py"
Task: "Create backend/middleware/ directory with __init__.py"
Task: "Create backend/schemas/ directory with __init__.py"
Task: "Create backend/services/ directory with __init__.py"
Task: "Create empty specs/features/ directory"
Task: "Create empty specs/api/ directory"
Task: "Create empty specs/database/ directory"
Task: "Create empty specs/ui/ directory"
```

## Parallel Example: User Story 6

```bash
# Frontend CLAUDE.md tasks (all parallel):
Task: "Create frontend/CLAUDE.md with Next.js 16 breaking changes section"
Task: "Add Better Auth integration section to frontend/CLAUDE.md"
Task: "Add API proxy pattern section to frontend/CLAUDE.md"
Task: "Add App Router architecture section to frontend/CLAUDE.md"
Task: "Add component patterns section to frontend/CLAUDE.md"
Task: "Add Tailwind CSS responsive patterns section to frontend/CLAUDE.md"
Task: "Add code standards section to frontend/CLAUDE.md"
Task: "Add reference to root CLAUDE.md in frontend/CLAUDE.md"
Task: "Add code examples to frontend/CLAUDE.md for async params pattern"

# Backend CLAUDE.md tasks (all parallel, can run simultaneously with frontend):
Task: "Create backend/CLAUDE.md with FastAPI application structure section"
Task: "Add SQLModel ORM patterns section to backend/CLAUDE.md"
Task: "Add JWT verification middleware section to backend/CLAUDE.md"
Task: "Add user isolation enforcement section to backend/CLAUDE.md"
Task: "Add database connection section to backend/CLAUDE.md"
Task: "Add API endpoint patterns section to backend/CLAUDE.md"
Task: "Add security requirements section to backend/CLAUDE.md"
Task: "Add CORS configuration section to backend/CLAUDE.md"
Task: "Add code examples to backend/CLAUDE.md for user isolation"
Task: "Add reference to root CLAUDE.md in backend/CLAUDE.md"
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T006)
3. Complete User Story 1: Project Structure (T007-T018)
4. Complete User Story 2: Environment Config (T019-T025)
5. Complete User Story 3: Architecture Docs (T026-T033)
6. **STOP and VALIDATE**: Verify directories exist, .env.example files complete, architecture documented
7. Foundation is now minimally viable - developers can start feature work

### Incremental Delivery

1. **Foundation Ready** (Setup + Foundational) → T001-T006 complete
2. **Structure Complete** (+ User Story 1) → T001-T018 complete → Developers can navigate project
3. **Config Complete** (+ User Story 2) → T001-T025 complete → Developers can configure environment
4. **Architecture Complete** (+ User Story 3) → T001-T033 complete → Developers understand system design (MVP!)
5. **Services Startable** (+ User Story 4) → T001-T042 complete → Developers can run Docker Compose
6. **Onboarding Complete** (+ User Story 5) → T001-T054 complete → New developers can self-onboard
7. **Guidance Complete** (+ User Story 6) → T001-T073 complete → Agents have layer-specific instructions
8. **Polish Complete** (+ Phase 9) → T001-T082 complete → All requirements validated

### Parallel Team Strategy

With multiple developers/agents:

1. **Team completes Setup + Foundational together** (T001-T006)
2. **Once Foundational done, distribute user stories**:
   - Developer A: User Story 1 (directory structure)
   - Developer B: User Story 2 (environment config)
   - Developer C: User Story 3 (architecture docs)
3. **Second wave** (after first 3 complete):
   - Developer D: User Story 4 (Docker Compose)
   - Developer E: User Story 5 (README)
   - Developer F: User Story 6 (component CLAUDE.md files)
4. **All converge on Polish phase** (T074-T082)

---

## Task Summary

**Total Tasks**: 82 tasks

**Task Count Per User Story**:
- Setup (Phase 1): 4 tasks
- Foundational (Phase 2): 2 tasks
- User Story 1 (P1 - Project Structure): 12 tasks
- User Story 2 (P1 - Environment Config): 7 tasks
- User Story 3 (P1 - Architecture Docs): 8 tasks
- User Story 4 (P2 - Docker Compose): 9 tasks
- User Story 5 (P2 - README Onboarding): 12 tasks
- User Story 6 (P3 - Component Guidance): 19 tasks
- Polish (Phase 9): 9 tasks

**Parallel Opportunities**:
- Setup: 3 tasks can run in parallel
- Foundational: 2 tasks can run in parallel
- User Story 1: 12 tasks can all run in parallel (100% parallelizable)
- User Story 3: 2 tasks can run in parallel initially
- User Story 4: 2 Dockerfile tasks can run in parallel
- User Story 6: 9 frontend tasks + 11 backend tasks can run in parallel (20 tasks total, 100% parallelizable)
- Polish: 6 tasks can run in parallel

**Total Parallelizable Tasks**: 44 tasks marked [P] (54% of all tasks)

**Suggested MVP Scope**:
- User Stories 1, 2, 3 (P1 priorities) = 27 implementation tasks + 6 foundation tasks = 33 tasks
- This delivers: Directory structure, environment configuration, architecture documentation
- Developers can then begin feature implementation with full foundation in place

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- No test tasks included (not requested in specification)
- All tasks include exact file paths for implementation
- Commit after each task or logical group of parallel tasks
- Stop at any checkpoint to validate story independently
- All FR-001 through FR-020 requirements mapped to tasks
- BETTER_AUTH_SECRET matching requirement enforced in multiple locations
- Next.js 16 breaking changes documented per FR-016
- CORS configuration requirements documented per FR-017
- httpOnly cookie strategy documented per FR-018
