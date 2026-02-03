# Tasks: Better Auth Integration with JWT & httpOnly Cookies

**Input**: Design documents from `/specs/003-better-auth/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are NOT requested in the specification. Focus on implementation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

This is a **web application** with frontend and backend:
- Frontend paths: `frontend/src/app/`, `frontend/src/components/`, `frontend/src/lib/`
- Backend paths: `backend/app/models/`, `backend/app/routes/`, `backend/app/dependencies/`, `backend/app/middleware/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation for both frontend and backend

- [X] T001 Install Better Auth packages in frontend: `better-auth`, `@better-auth/jwt`, `jose`
- [X] T002 Install PyJWT package in backend: `pyjwt`, `python-multipart`
- [X] T003 [P] Generate secure BETTER_AUTH_SECRET using `openssl rand -hex 32`
- [X] T004 [P] Create `frontend/.env.local` with BETTER_AUTH_SECRET, DATABASE_URL, NEXT_PUBLIC_BACKEND_URL
- [X] T005 [P] Create `backend/.env` with BETTER_AUTH_SECRET and DATABASE_URL (must match frontend secret)
- [X] T006 Verify DATABASE_URL points to Neon PostgreSQL database

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core authentication infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Create Better Auth configuration in `frontend/src/lib/auth.ts` with JWT plugin, PostgreSQL adapter, httpOnly cookie settings
- [X] T008 Create Better Auth API route handler in `frontend/src/app/api/auth/[...all]/route.ts` using `toNextJsHandler`
- [X] T009 Run Better Auth database migrations: `npx better-auth migrate` to create user, session, account, verification tables
- [X] T010 Update tasks table to reference users: `ALTER TABLE tasks ALTER COLUMN user_id TYPE VARCHAR(255)` and add foreign key constraint to user.id
- [X] T011 [P] Create JWT auth dependencies in `backend/app/dependencies/auth.py` with `get_current_user_id` and `verify_user_id_match` functions
- [X] T012 [P] Update FastAPI main.py to configure CORS with credentials: allow specific origins, credentials=True, no wildcard
- [X] T013 Create API proxy route in `frontend/src/app/api/proxy/[...path]/route.ts` to read httpOnly cookies and forward to backend with Authorization header
- [X] T014 [P] Create API client helper in `frontend/src/lib/api-client.ts` with functions for fetchTasks, createTask, updateTask, deleteTask using proxy

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - New User Registration (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts with email/password and automatically log in

**Independent Test**: Navigate to `/signup`, enter valid credentials (email + 8+ char password), verify account created and user redirected to `/tasks`

### Implementation for User Story 1

- [X] T015 [P] [US1] Create signup page component in `frontend/src/app/(auth)/signup/page.tsx` with email and password input fields
- [X] T016 [US1] Add form validation to signup page: email format check, password minimum 8 characters, display validation errors
- [X] T017 [US1] Implement signup form submission: POST to `/api/auth/signup`, handle success (redirect to /dashboard), handle errors (duplicate email, invalid format)
- [X] T018 [US1] Style signup page with Tailwind CSS: responsive layout (mobile 375px, tablet 768px, desktop 1024px+), centered form, clear error messages
- [X] T019 [US1] Add "Already have an account? Log in" link to signup page pointing to `/auth/login`

**Checkpoint**: User Story 1 complete - users can sign up, accounts are created in database, automatic login works

---

## Phase 4: User Story 2 - Returning User Login (Priority: P1) 🎯 MVP

**Goal**: Enable existing users to authenticate with email/password and access their tasks

**Independent Test**: Create test user via signup, log out, then log in with correct credentials and verify access to user's tasks only

### Implementation for User Story 2

- [X] T020 [P] [US2] Create login page component in `frontend/src/app/(auth)/login/page.tsx` with email and password input fields
- [X] T021 [US2] Add form validation to login page: email format check, required password field, display validation errors
- [X] T022 [US2] Implement login form submission: POST to `/api/auth/login` with credentials='include', handle success (redirect to /dashboard), handle errors (invalid credentials with generic message)
- [X] T023 [US2] Style login page with Tailwind CSS: responsive layout matching signup page, centered form, clear error messages
- [X] T024 [US2] Add "Don't have an account? Sign up" link to login page pointing to `/auth/signup`
- [X] T025 [US2] Verify httpOnly cookie `better-auth.session_token` is set after successful login with 7-day expiration

**Checkpoint**: User Story 2 complete - existing users can log in and receive JWT tokens in httpOnly cookies

---

## Phase 5: User Story 4 - User Data Isolation (Priority: P1) 🎯 Security Critical

**Goal**: Enforce strict user data isolation at backend - users can only access their own data even with API manipulation

**Independent Test**: Create two users with different tasks, log in as User A, attempt to access User B's task endpoint (e.g., `/api/user-b-id/tasks`), verify backend returns 403 Forbidden

### Implementation for User Story 4

- [X] T026 [P] [US4] Update task routes in `backend/app/routes/tasks.py` to use `verify_user_id_match` dependency on all endpoints (GET /tasks, POST /tasks, GET /tasks/{id}, PUT /tasks/{id}, DELETE /tasks/{id}, PATCH /tasks/{id}/complete)
- [X] T027 [US4] Ensure all task database queries filter by authenticated user_id: `WHERE user_id = <jwt_user_id>`
- [X] T028 [US4] Verify JWT verification returns 401 Unauthorized for missing/invalid tokens
- [X] T029 [US4] Verify user_id mismatch returns 403 Forbidden with message "Access denied: user_id mismatch"
- [X] T030 [US4] Test user isolation: create two users, log in as User A, verify cannot access User B's tasks via API proxy

**Checkpoint**: User Story 4 complete - backend enforces user data isolation, JWT verification works, 401/403 errors returned correctly

---

## Phase 6: User Story 3 - Secure Session Management (Priority: P2)

**Goal**: Provide secure session handling with automatic token inclusion, logout functionality, and session persistence

**Independent Test**: Log in, make API requests (verify token auto-included), log out, verify session cleared and API requests fail with 401

### Implementation for User Story 3

- [X] T031 [P] [US3] Create logout button component in `frontend/src/components/auth/logout-button.tsx` with POST to `/api/auth/logout`
- [X] T032 [US3] Implement logout functionality: clear httpOnly cookie, redirect to `/auth/login`, verify subsequent API requests fail with 401
- [X] T033 [US3] Add logout button to task dashboard layout (visible when user is logged in)
- [X] T034 [US3] Verify session persistence: log in, close browser, reopen within 7 days, verify user still logged in
- [X] T035 [US3] Implement expired token handling: when JWT expires (after 7 days), redirect to `/auth/login` with message "Your session has expired. Please log in again"
- [X] T036 [US3] Verify API proxy automatically includes JWT token from httpOnly cookie in Authorization header for all requests (GET, POST, PUT, DELETE, PATCH)

**Checkpoint**: User Story 3 complete - users can log out, sessions persist across browser sessions, expired tokens handled gracefully

---

## Phase 7: User Story 5 - Protected Routes (Priority: P2)

**Goal**: Redirect unauthenticated users to login page, redirect authenticated users away from auth pages

**Independent Test**: Access `/tasks` without login (verify redirect to `/login`), log in, access `/login` (verify redirect to `/tasks`)

### Implementation for User Story 5

- [X] T037 [P] [US5] Create session check utility in `frontend/src/lib/auth-utils.ts` to read current session via `/api/auth/session`
- [X] T038 [US5] Create protected route wrapper component in `frontend/src/components/auth/protected-route.tsx` that checks session and redirects to `/auth/login` if not authenticated
- [X] T039 [US5] Apply protected route wrapper to task dashboard page in `frontend/src/app/(dashboard)/tasks/page.tsx`
- [X] T040 [US5] Implement redirect logic on login/signup pages: if user already authenticated, redirect to `/dashboard`
- [X] T041 [US5] Implement "redirect after login" functionality: save intended route before redirecting to login, restore after successful authentication
- [X] T042 [US5] Display "Please log in to continue" message when unauthenticated user is redirected to login page
- [X] T043 [US5] Handle expired/invalid JWT tokens: detect on protected route access, clear cookie, redirect to `/auth/login`

**Checkpoint**: User Story 5 complete - protected routes enforce authentication, auth pages redirect logged-in users, seamless redirect-after-login flow

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final touches, error handling improvements, and documentation

- [X] T044 [P] Add loading states to login and signup forms during submission
- [X] T045 [P] Add loading state to logout button during logout operation
- [X] T046 [P] Improve error messages: display specific validation errors from Better Auth (email already exists, password too short, invalid email format)
- [X] T047 [P] Add accessibility attributes: aria-labels for form fields, error announcements, keyboard navigation support
- [X] T048 Verify all forms work on mobile (375px), tablet (768px), and desktop (1024px+) breakpoints
- [X] T049 [P] Add rate limiting consideration notes to documentation (out of scope for implementation but document for future)
- [X] T050 [P] Document environment variable requirements in README.md (BETTER_AUTH_SECRET, DATABASE_URL, NEXT_PUBLIC_BACKEND_URL)
- [X] T051 Verify CORS configuration works with frontend-backend communication (credentials included, no CORS errors in browser)
- [X] T052 Final integration test: complete end-to-end flow (signup → login → access tasks → logout → verify session cleared)

**Final Checkpoint**: All user stories complete and polished - authentication system fully functional

---

## Dependencies & Execution Order

### User Story Dependency Graph

```
Phase 1 (Setup) → Phase 2 (Foundational)
                       ↓
    ┌──────────────────┴───────────────────┐
    │                                      │
    ↓                                      ↓
US1: Signup (P1) 🎯                    US2: Login (P1) 🎯
    │                                      │
    ↓                                      ↓
US4: Data Isolation (P1) 🎯 Security Critical
    │
    ↓
    ├─→ US3: Session Management (P2)
    │
    └─→ US5: Protected Routes (P2)
         ↓
    Phase 8: Polish
```

**Execution Strategy**:

1. **Sequential**: Phase 1 (Setup) → Phase 2 (Foundational) MUST complete first
2. **Parallel**: After Phase 2, US1 (Signup) and US2 (Login) can be implemented in parallel
3. **Blocking**: US4 (Data Isolation) MUST complete before US3 and US5 (depends on backend JWT verification)
4. **Parallel**: US3 (Session Management) and US5 (Protected Routes) can be implemented in parallel after US4
5. **Final**: Phase 8 (Polish) after all user stories complete

### MVP Scope (Minimum Viable Product)

**Recommended MVP**: Phase 1 + Phase 2 + Phase 3 (US1: Signup) + Phase 4 (US2: Login) + Phase 5 (US4: Data Isolation)

**Rationale**: These three P1 user stories provide:
- User registration (US1)
- User login (US2)
- Secure data isolation (US4)

This is the minimum needed for a functional multi-user system. US3 and US5 enhance UX but US1+US2+US4 deliver core authentication.

### Parallel Execution Examples

**Within Phase 3 (US1: Signup)**:
- T015 (signup page component) can run in parallel with T018 (styling) initially
- T016 (form validation) depends on T015
- T017 (form submission) depends on T015 and T016

**Within Phase 4 (US2: Login)**:
- T020 (login page component) can run in parallel with T023 (styling) initially
- T021 (form validation) depends on T020
- T022 (form submission) depends on T020 and T021

**Across User Stories (after Phase 2)**:
- All of Phase 3 (US1) can run in parallel with all of Phase 4 (US2)
- Phase 5 (US4) must wait for US1 and US2 to complete (needs working login for testing)

**Within Phase 6 (US3)**:
- T031 (logout button component) and T034 (session persistence verification) can run in parallel
- T032 (logout functionality) depends on T031
- T036 (API proxy verification) is independent and can run in parallel

**Within Phase 7 (US5)**:
- T037 (session check utility), T040 (redirect logic), and T042 (message display) can run in parallel initially
- T038 (protected route wrapper) depends on T037
- T039 (apply wrapper) depends on T038

**Within Phase 8 (Polish)**:
- T044, T045, T046, T047 (UI improvements) can all run in parallel
- T048 (responsive verification), T049 (documentation), T050 (README update) can run in parallel

---

## Implementation Strategy

### Incremental Delivery Approach

1. **Sprint 1: Foundation + MVP Core (US1 + US2)**
   - Complete Phase 1 (Setup) and Phase 2 (Foundational)
   - Implement US1 (Signup) - delivers new user registration
   - Implement US2 (Login) - delivers existing user authentication
   - **Deliverable**: Users can create accounts and log in

2. **Sprint 2: Security (US4)**
   - Implement US4 (Data Isolation) - enforces backend security
   - **Deliverable**: Multi-user system with data isolation

3. **Sprint 3: UX Enhancement (US3 + US5)**
   - Implement US3 (Session Management) - logout, session persistence, expiration
   - Implement US5 (Protected Routes) - route protection, redirects
   - **Deliverable**: Complete authentication UX

4. **Sprint 4: Polish**
   - Complete Phase 8 (Polish & Cross-Cutting)
   - **Deliverable**: Production-ready authentication system

### Task Execution Checklist

Before starting implementation:
- [ ] All design documents reviewed (plan.md, spec.md, data-model.md, contracts/)
- [ ] Database accessible (Neon PostgreSQL connection string in .env)
- [ ] Frontend and backend projects initialized
- [ ] BETTER_AUTH_SECRET generated and identical in both .env files

During implementation:
- [ ] Follow task order within each phase
- [ ] Mark tasks as complete only when acceptance criteria met
- [ ] Test each user story independently after its phase completes
- [ ] Verify no user story implementation leaks into another story's phase

After implementation:
- [ ] All 5 user stories independently testable and functional
- [ ] End-to-end authentication flow works (signup → login → tasks → logout)
- [ ] User data isolation verified (cannot access other users' data)
- [ ] Session management works (persistence, expiration, logout)
- [ ] Protected routes enforce authentication

---

## Summary

**Total Tasks**: 52
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundational): 8 tasks
- Phase 3 (US1 - Signup): 5 tasks
- Phase 4 (US2 - Login): 6 tasks
- Phase 5 (US4 - Data Isolation): 5 tasks
- Phase 6 (US3 - Session Management): 6 tasks
- Phase 7 (US5 - Protected Routes): 7 tasks
- Phase 8 (Polish): 9 tasks

**Parallel Opportunities**: 23 tasks marked with [P] can run in parallel with other tasks

**Independent Test Criteria**:
- US1: Navigate to /signup, create account, verify redirect to /tasks
- US2: Log out, log in with credentials, verify access to tasks
- US3: Log in, make API requests, log out, verify 401 on subsequent requests
- US4: Create two users, verify User A cannot access User B's data (403 Forbidden)
- US5: Access /tasks without login, verify redirect to /login; log in, access /login, verify redirect to /tasks

**MVP Scope**: Phases 1, 2, 3, 4, 5 (US1 Signup + US2 Login + US4 Data Isolation) = 25 tasks

**Format Validation**: ✅ All tasks follow checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`
