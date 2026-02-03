---
id: 0003
title: better-auth-integration-implementation-plan
stage: plan
date: 2026-02-03
surface: agent
model: claude-sonnet-4-5
feature: 004-fix-better-auth-integration
branch: 004-fix-better-auth-integration
user: developer
command: /sp.plan
labels: ["implementation-plan", "better-auth", "bug-fix", "api-migration", "testing"]
links:
  spec: specs/004-fix-better-auth-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-fix-better-auth-integration/plan.md
  - specs/004-fix-better-auth-integration/research.md
  - specs/004-fix-better-auth-integration/quickstart.md
  - specs/004-fix-better-auth-integration/data-model.md
tests:
  - Constitution Check passed (7/7 principles compliant)
---

## Prompt

User executed: `/sp.plan`

Context: Following specification (PHR 0001) and clarification (PHR 0002) completion, user initiated planning workflow to design implementation approach for fixing Better Auth v1.4.18 API compatibility issues.

Command executed: /sp.plan

## Response snapshot

Created comprehensive implementation plan for Better Auth API migration with 4 phases:

**Phase 0 - Research & Documentation**:
- Documented Better Auth `createAuthClient` API patterns
- Documented FastAPI dependency override testing strategy
- Documented pytest retry configuration (3 retries per clarification)
- Documented structured logging patterns (FR-011 requirement)
- Created `research.md` with API examples and rationale

**Phase 1 - Frontend Migration** (6 sub-phases):
1. CREATE `auth-client.ts` (foundational - blocks all frontend fixes)
2. FIX login page (replace `useSignIn` with `authClient.signIn.email()`)
3. FIX signup page (replace `useRegister` with `authClient.signUp.email()`)
4. FIX logout button (replace `useSignOut` with `authClient.signOut()`)
5. FIX protected route (replace `useSession` with `authClient.useSession()`)
6. CREATE frontend logger (structured logging for auth events)

**Phase 2 - Backend Test Fixes** (5 sub-phases):
1. FIX `conftest.py` (add dependency override - foundational)
2. FIX `test_auth_flow.py` (remove JWT token generation, use override)
3. FIX `test_session_management.py` (use dependency override pattern)
4. ADD pytest retry config (implement 3-retry strategy)
5. CREATE backend logger (structured logging for auth events)

**Phase 3 - Integration Testing**:
- Frontend build verification (0 errors target)
- Backend test execution (33/33 passing target)
- End-to-end manual testing checklist
- Structured logging verification

**Phase 4 - Documentation**:
- Quickstart guide (migration patterns)
- Frontend CLAUDE.md updates (new API examples)
- Backend tests README (dependency override documentation)

**Key Decisions**:
1. Use `app.dependency_overrides` for test auth (vs real JWT tokens) - simpler, faster, more maintainable
2. Manual state management in components (vs deprecated hooks) - more control over loading states
3. Automatic retry config for all tests (vs per-test markers) - handles flaky tests transparently

**Critical Path Identified**:
- `auth-client.ts` blocks all frontend fixes
- `conftest.py` blocks all backend test fixes
- Sequential frontend → backend → integration testing

**Deliverables Created**:
- `plan.md` (1250 lines) - Complete implementation plan with code examples
- `research.md` - API research and technical decisions
- `quickstart.md` - Developer quick reference
- `data-model.md` - No changes (bug fix confirmation)

## Outcome

- ✅ Impact: Created production-ready implementation plan covering 11 file changes + 3 new files + documentation; unblocks task generation and implementation
- 🧪 Tests: Constitution Check passed 7/7 principles; plan validated against spec requirements
- 📁 Files: Created 4 planning artifacts (plan.md, research.md, quickstart.md, data-model.md)
- 🔁 Next prompts: Run `/sp.tasks` to generate actionable task list with exact file paths and acceptance criteria
- 🧠 Reflection: Plan emphasizes surgical migration (API changes only) over refactoring; dependency override pattern significantly simplifies backend testing; structured logging adds scope but improves production supportability

## Evaluation notes (flywheel)

- Failure modes observed: None - plan completed successfully with all Phase 0/1 artifacts
- Graders run and results (PASS/FAIL): Constitution Check - PASS (7/7), Spec Alignment - PASS (all FR/SC requirements addressed)
- Prompt variant (if applicable): Standard /sp.plan workflow with Plan agent for comprehensive analysis
- Next experiment (smallest change to try): Validate that dependency override pattern works in actual test environment during `/sp.implement` phase
