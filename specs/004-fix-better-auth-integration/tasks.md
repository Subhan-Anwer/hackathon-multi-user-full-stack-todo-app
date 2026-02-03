# Implementation Tasks: Fix Better Auth Integration

**Feature**: Fix Better Auth Integration
**Branch**: `004-fix-better-auth-integration`
**Date**: 2026-02-03
**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)

## Overview

This task list implements the Better Auth v1.4.18 API migration to fix 19 frontend build errors and 19 backend test failures. Tasks are organized by user story to enable independent implementation and testing.

**Tech Stack**:
- Frontend: TypeScript 5.x, Next.js 16+, Better Auth 1.4.18, React 19
- Backend: Python 3.11, FastAPI, SQLModel, pytest
- Database: Neon PostgreSQL (no schema changes)

**Total Tasks**: 16 tasks
- Phase 1 (Setup): 0 tasks (no setup needed - existing project)
- Phase 2 (Foundational): 2 tasks (blocking all user stories)
- Phase 3 (User Story 1 - Frontend Build): 6 tasks
- Phase 4 (User Story 2 - Backend Tests): 5 tasks
- Phase 5 (User Story 3 - E2E Auth): 1 task
- Phase 6 (Polish): 2 tasks

---

## Phase 1: Setup

**Status**: ✅ Complete (no setup needed)

This is a bug fix on an existing project. All infrastructure (Next.js, FastAPI, Better Auth library, database) is already configured.

---

## Phase 2: Foundational Tasks (Blocking)

**Objective**: Create foundational auth client and test infrastructure that all user stories depend on

**Completion Criteria**:
- `frontend/src/lib/auth-client.ts` exports working `authClient` instance
- `backend/tests/conftest.py` provides `client` fixture with mocked authentication

### Tasks

- [x] T001 CREATE central Better Auth client in `frontend/src/lib/auth-client.ts` using `createAuthClient` from `better-auth/react` with baseURL configuration
- [x] T002 FIX test authentication fixtures in `backend/tests/conftest.py` by adding `get_current_user_id` dependency override returning "user-123"

**Dependencies**: None (foundational tasks)

**Acceptance**:
- T001: Import `authClient` in any component without errors; TypeScript type hints work
- T002: Run `pytest --collect-only` shows fixtures loaded without errors

---

## Phase 3: User Story 1 - Developer Builds Frontend Successfully (Priority: P1)

**Story Goal**: Fix 19 frontend Turbopack build errors by migrating auth components to Better Auth v1.4.18 API

**Independent Test**:
```bash
cd frontend && npm run build
```
**Expected**: 0 errors, production artifacts in `.next/` directory

**Why Independent**: All auth component fixes are in frontend codebase only; backend can remain broken

**Acceptance Scenarios**:
1. Build completes with zero Turbopack errors
2. TypeScript compilation passes with no type errors
3. All JavaScript bundles created without warnings

### Tasks

- [x] T003 [P] [US1] FIX login page `frontend/src/app/(auth)/login/page.tsx` - Replace `useSignIn` import with `authClient` from `@/lib/auth-client`; use `authClient.signIn.email()` method with manual loading state
- [x] T004 [P] [US1] FIX signup page `frontend/src/app/(auth)/signup/page.tsx` - Replace `useRegister` import with `authClient`; use `authClient.signUp.email()` method with manual loading state
- [x] T005 [P] [US1] FIX logout button `frontend/src/components/auth/logout-button.tsx` - Replace `useSignOut` hook with `authClient.signOut()` call and manual `useState` for loading
- [x] T006 [P] [US1] FIX protected route `frontend/src/components/auth/protected-route.tsx` - Replace `useSession` import with `authClient.useSession()` accessed through client object
- [x] T007 [P] [US1] CREATE structured auth logger in `frontend/src/lib/logger.ts` with methods for signInAttempt, signInSuccess, signInFailure, signOutSuccess, sessionCheck (JSON format logs)
- [x] T008 [US1] INTEGRATE logger calls in login/signup/logout components - Add `authLogger` calls at appropriate points (before/after auth operations)

**Dependencies**:
- All tasks depend on T001 (auth-client.ts must exist first)
- T003-T006 are parallel (independent files)
- T007 is parallel with T003-T006 (separate file)
- T008 depends on T003-T007 (needs all components + logger)

**Parallel Execution**: T003, T004, T005, T006, T007 can run simultaneously (5 parallel tasks)

**Story Completion Test**:
```bash
cd frontend
npm run build  # Should show "Compiled successfully" with 0 errors
npm run dev    # Pages should load without console errors
```

---

## Phase 4: User Story 2 - Developer Runs Backend Tests Successfully (Priority: P1)

**Story Goal**: Fix 19 failing backend authentication tests while maintaining 14 passing database tests

**Independent Test**:
```bash
cd backend && pytest -v
```
**Expected**: 33/33 tests passing (14 DB + 19 auth)

**Why Independent**: Backend test fixes don't require frontend changes; can validate with mocked auth

**Acceptance Scenarios**:
1. All 19 auth tests pass without failures
2. JWT token validation tests accept valid tokens, reject invalid
3. Zero deprecation warnings in test output
4. Database tests remain passing (14/14)

### Tasks

- [x] T009 [P] [US2] FIX auth flow tests in `backend/tests/test_auth_flow.py` - Remove JWT token generation code; use `client` fixture with dependency override; test user isolation with `client_user_456` fixture
- [x] T010 [P] [US2] FIX session management tests in `backend/tests/test_session_management.py` - Replace JWT mocking with dependency override pattern; use `client` fixture for all test requests
- [x] T011 [P] [US2] ADD pytest retry configuration in `backend/pyproject.toml` - Add `pytest-rerunfailures` dependency and configure `reruns = 3`, `reruns_delay = 1` in pytest.ini_options
- [x] T012 [P] [US2] CREATE backend auth logger in `backend/app/utils/logger.py` - Implement `AuthLogger` class with `log_event()`, `token_validation_success()`, `token_validation_failure()`, `session_check()` methods (JSON format to file)
- [x] T013 [US2] INTEGRATE backend logging in `backend/app/middleware/auth.py` and `backend/app/dependencies/auth.py` - Add `auth_logger` calls in JWT verification paths

**Dependencies**:
- All tasks depend on T002 (conftest.py must have overrides)
- T009-T012 are parallel (independent files)
- T013 depends on T012 (needs logger created)

**Parallel Execution**: T009, T010, T011, T012 can run simultaneously (4 parallel tasks)

**Story Completion Test**:
```bash
cd backend
pytest tests/test_auth_flow.py tests/test_session_management.py -v
# Should show all green, 19/19 passing

pytest  # Run all tests
# Should show 33/33 passing (14 DB + 19 auth)
```

---

## Phase 5: User Story 3 - End User Authenticates Successfully (Priority: P2)

**Story Goal**: Verify end-to-end authentication flow works from user perspective

**Independent Test**:
1. Start backend: `cd backend && uvicorn app.main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Navigate to http://localhost:3000/auth/signup
4. Create account → verify redirect to /dashboard
5. Logout → verify redirect to /login
6. Login → verify redirect to /dashboard
7. Create task → verify task saved
8. Logout → verify session cleared

**Why Independent**: Tests real user flow; can validate after US1+US2 complete

**Acceptance Scenarios**:
1. Signup creates account and redirects to dashboard
2. Login with valid credentials succeeds
3. Protected routes require authentication
4. Logout clears session
5. Session expiry shows "Session expired" message

### Tasks

- [x] T014 [US3] MANUAL E2E TEST - Execute full authentication flow following quickstart.md testing checklist; verify signup, login, protected routes, logout, session persistence

**Dependencies**:
- Depends on T001-T008 (frontend must build and work)
- Depends on T002 (backend auth must work, though tests validate this)

**Story Completion Test**: Manual checklist in Phase 3.3 of plan.md - all items checked

---

## Phase 6: Polish & Cross-Cutting Concerns

**Objective**: Documentation and final validation

### Tasks

- [x] T015 [P] UPDATE `frontend/CLAUDE.md` - Add Better Auth v1.4.18 API section with code examples for `createAuthClient`, `signIn.email()`, `signOut()`, `useSession()`
- [x] T016 [P] CREATE `backend/tests/README.md` - Document dependency override pattern, explain fixtures (`client`, `client_user_456`), pytest retry configuration, and cross-user testing examples

**Dependencies**:
- T015-T016 are parallel (independent files)
- Can run anytime after Phase 3-5 tasks complete

**Acceptance**:
- Documentation includes working code examples
- README explains fixture usage clearly
- New team members can understand auth testing approach

---

## Task Dependencies Visualization

```
Setup Phase: (none - existing project)

Foundational Phase:
T001 (auth-client.ts) ─┬─> T003 (login page)
                       ├─> T004 (signup page)
                       ├─> T005 (logout button)
                       ├─> T006 (protected route)
                       ├─> T007 (logger) ──────┐
                       └──────────────────────┐ │
                                              │ │
T002 (conftest.py) ────┬─> T009 (auth tests) │ │
                       ├─> T010 (session tests)│
                       ├─> T011 (pytest config)│
                       └─> T012 (backend logger)┘
                                 │               │
                                 └───> T013 <────┘

User Story 1 (Frontend):
T001 → [T003, T004, T005, T006, T007] → T008

User Story 2 (Backend):
T002 → [T009, T010, T011, T012] → T013

User Story 3 (E2E):
[T001-T013] → T014

Polish:
[T003-T013] → [T015, T016]
```

---

## Parallel Execution Opportunities

### User Story 1 (Frontend) - 5 Parallel Tasks
After T001 completes, run in parallel:
- T003 (login page) + T004 (signup page) + T005 (logout) + T006 (protected route) + T007 (logger)

### User Story 2 (Backend) - 4 Parallel Tasks
After T002 completes, run in parallel:
- T009 (auth tests) + T010 (session tests) + T011 (pytest config) + T012 (backend logger)

### Polish Phase - 2 Parallel Tasks
After all story tasks complete:
- T015 (frontend docs) + T016 (backend docs)

**Total Parallel Opportunities**: 11 tasks can be parallelized (saves ~60% time vs sequential)

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**User Story 1 ONLY** = Frontend Build Fix
- Tasks: T001, T003-T008 (8 tasks)
- Delivers: Frontend builds successfully (unblocks deployment)
- Independent: Backend can remain broken temporarily
- Time: ~1-1.5 hours

### Incremental Delivery

1. **MVP (US1)**: T001 → T003-T007 parallel → T008 → Validate build
2. **Backend Tests (US2)**: T002 → T009-T012 parallel → T013 → Validate tests
3. **E2E Validation (US3)**: T014 → Manual testing
4. **Polish**: T015-T016 parallel → Documentation complete

### Critical Path

```
T001 (30 min) → T003-T007 parallel (45 min) → T008 (15 min) = 1.5 hours MVP
              ↓
T002 (20 min) → T009-T012 parallel (40 min) → T013 (15 min) = 1.25 hours backend
              ↓
T014 (30 min E2E) + [T015, T016] parallel (30 min) = 1 hour finish

Total: 3.75 hours (with parallelization)
Sequential: 6.5 hours (without parallelization)
```

---

## Success Metrics

### User Story 1 Success Criteria
- [ ] Frontend build: 0 errors (down from 19)
- [ ] TypeScript compilation: No type errors
- [ ] `npm run dev` starts without crashes
- [ ] All auth pages load in browser

### User Story 2 Success Criteria
- [ ] Backend tests: 33/33 passing (14 DB + 19 auth)
- [ ] pytest output: No deprecation warnings
- [ ] Cross-user tests: 403 responses verified
- [ ] Test retry working: Reruns visible in verbose output

### User Story 3 Success Criteria
- [ ] Signup flow: Account created, redirects to dashboard
- [ ] Login flow: JWT cookie set, dashboard accessible
- [ ] Logout flow: Cookie cleared, redirect to login
- [ ] Protected routes: Unauthenticated users redirected
- [ ] Session expiry: "Session expired" message shown

### Overall Success
- [ ] All 16 tasks completed
- [ ] All 3 user stories independently tested and passing
- [ ] Zero regressions (existing features still work)
- [ ] Documentation updated

---

## Validation Commands

### After Each User Story

**User Story 1 (Frontend)**:
```bash
cd frontend
npm run build  # Must show: "Compiled successfully" with 0 errors
npm run dev    # Must start on http://localhost:3000
# Open browser: Navigate to /auth/login → page should load
```

**User Story 2 (Backend)**:
```bash
cd backend
pytest tests/test_auth_flow.py -v  # Must show: 10 passed
pytest tests/test_session_management.py -v  # Must show: 9 passed
pytest  # Must show: 33 passed total
```

**User Story 3 (E2E)**:
```bash
# Terminal 1
cd backend && uvicorn app.main:app --reload

# Terminal 2
cd frontend && npm run dev

# Browser: Execute manual test checklist from plan.md Phase 3.3
```

---

## Risk Mitigation

### High-Risk Tasks (Monitor Closely)

1. **T001 (auth-client.ts)** - Blocks entire frontend
   - **Risk**: Wrong API usage breaks all components
   - **Mitigation**: Test import immediately after creation
   - **Rollback**: Use example from quickstart.md

2. **T002 (conftest.py)** - Blocks entire backend testing
   - **Risk**: Dependency override conflicts
   - **Mitigation**: Run `pytest --collect-only` to validate fixtures
   - **Rollback**: Remove override, tests will still fail but not crash

3. **T008 (logger integration)** - Could break auth flows
   - **Risk**: Logger errors crash auth operations
   - **Mitigation**: Wrap logger calls in try/except
   - **Rollback**: Comment out logger calls, keep empty logger file

### Flaky Tests

**If tests fail intermittently**:
- T011 adds automatic retry (3 attempts)
- Review pytest logs with `pytest -v --reruns-report`
- Investigate patterns (network timing, DB connections)

---

## Rollback Plan

If >50% of tasks fail or introduce regressions:

### Option 1: Feature Branch Rollback
```bash
git checkout master
git branch -D 004-fix-better-auth-integration
# Restart planning with lessons learned
```

### Option 2: Partial Rollback
- Keep completed user stories (e.g., if US1 works, keep it)
- Revert failing stories only
- Deploy working parts, plan fixes for rest

### Option 3: Dependency Downgrade
```bash
cd frontend
npm install better-auth@1.3.0  # Previous stable version
git checkout -- <auth files>    # Revert to old API
```

---

## Notes

**Estimated Timeline**: 3.75 hours with parallelization, 6.5 hours sequential

**Parallel-Friendly**: 11 of 16 tasks (69%) can be parallelized

**Testing Approach**: No automated tests needed (bug fix validates existing tests)

**Breaking Changes**: None - maintains backward compatibility

**Documentation**: Quickstart.md and plan.md provide detailed code examples for each task

---

**Task List Version**: 1.0
**Last Updated**: 2026-02-03
**Status**: Ready for `/sp.implement`

**Next Command**: `/sp.implement` to execute tasks in dependency order with automatic progress tracking
