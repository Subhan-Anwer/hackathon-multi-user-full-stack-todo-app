---
id: 0003
title: Better Auth implementation planning
stage: plan
date: 2026-02-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-better-auth
branch: 003-better-auth
user: claude-code
command: /sp.plan
labels: ["authentication", "better-auth", "jwt", "planning", "architecture", "security"]
links:
  spec: specs/003-better-auth/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-better-auth/plan.md
  - specs/003-better-auth/research.md
  - specs/003-better-auth/data-model.md
  - specs/003-better-auth/quickstart.md
  - specs/003-better-auth/contracts/auth.openapi.yaml
  - specs/003-better-auth/contracts/proxy.openapi.yaml
tests:
  - Constitution Check (all 7 principles passed)
  - Research quality validation (comprehensive documentation with references)
---

## Prompt

Create:
1. Authentication flow diagram:
   - User submits credentials → Better Auth
   - Better Auth validates → Issues JWT
   - JWT stored in httpOnly cookie
   - Frontend makes API call → Proxy reads cookie
   - Proxy forwards with Authorization header
   - Backend verifies JWT → Returns data

2. Frontend auth components:
   - Better Auth configuration with JWT plugin
   - API route handlers for Better Auth
   - Login form component
   - Signup form component
   - Logout functionality
   - Protected route wrapper

3. httpOnly Cookie Proxy:
   - API route at /api/proxy/[...path]
   - Reads auth token from cookies (server-side)
   - Forwards to backend with Authorization header
   - Handles all HTTP methods (GET, POST, PUT, DELETE, PATCH)

4. Backend JWT verification:
   - Middleware to verify JWT signature
   - Extract user_id from token payload
   - Compare with user_id in URL
   - Return 401 for invalid/missing token
   - Return 403 for user_id mismatch

Decisions needing documentation:
- Cookie storage strategy → httpOnly (most secure)
- Token expiration → 7 days (balance security vs UX)
- Error handling → Generic messages (don't leak info)
- Redirect strategy → Login page with callback URL

Testing strategy:
- Test signup creates user and logs in
- Test login issues valid JWT
- Test logout clears token
- Test invalid token returns 401
- Test mismatched user_id returns 403
- Test session persistence across refreshes
- Test protected routes redirect to login

Technical details:
- Use 'sub' field in JWT for user_id
- Set httpOnly, secure, sameSite cookie attributes
- Handle expired tokens gracefully
- Include credentials: 'include' in fetch calls

## Response snapshot

Created comprehensive implementation plan following Spec-Kit Plus workflow:

**Phase 0: Research (Complete)**
- Research agent investigated Better Auth architecture, Next.js proxy patterns, FastAPI JWT verification
- Discovered PyJWT is actively maintained (python-jose abandoned since 2021)
- Documented cookie security patterns, CORS configuration, database schema integration
- Created 1709-line comprehensive research.md with official documentation references
- Merged agent-generated research with manual decision summary table

**Phase 1: Design & Contracts (Complete)**
- Created data model with 3 entities: User, Session, JWT Token (transient)
- Generated OpenAPI contracts for auth endpoints (signup, login, logout, session)
- Generated proxy API contract for cookie-to-header forwarding
- Defined database relationships and Better Auth table structure
- Created quickstart guide with step-by-step implementation instructions

**Technical Architecture**:
- Frontend: Better Auth + JWT plugin, Next.js Edge runtime proxy, httpOnly cookies
- Backend: PyJWT dependency injection, user_id validation, CORS with credentials
- Database: Better Auth auto-generates user, session, account, verification tables
- Security: Shared BETTER_AUTH_SECRET, user data isolation, 401/403 error handling

**Constitution Check**: ✅ All 7 principles satisfied
- Spec-driven development (spec.md created first)
- Zero manual coding (implementation via /sp.tasks)
- User data isolation (JWT verification + user_id comparison)
- JWT-based authentication (Better Auth with JWT plugin)
- RESTful API conventions (consistent endpoints and status codes)
- Responsive frontend design (Tailwind CSS mobile-first)
- MVP focus (excludes password reset, 2FA, OAuth, rate limiting)

**Key Architectural Decisions**:
1. Better Auth over NextAuth.js (modern, Next.js 16 optimized, automatic migrations)
2. PyJWT over python-jose (actively maintained, Python 3.10+ compatible)
3. Dependency injection over middleware (granular control, testability)
4. httpOnly cookies over localStorage (XSS protection, secure by default)
5. 7-day token expiration (balance security and UX without refresh tokens)

## Outcome

- ✅ Impact: Complete authentication architecture designed with Better Auth, JWT tokens, httpOnly cookies, and FastAPI backend integration. Ready for task breakdown and implementation.
- 🧪 Tests: Constitution Check (7/7 passed), Research quality validation (comprehensive with references)
- 📁 Files: 6 planning artifacts (plan.md, research.md 1709 lines, data-model.md, quickstart.md, 2 OpenAPI contracts)
- 🔁 Next prompts: /sp.tasks (generate implementation tasks), /sp.adr (document architectural decisions if needed)
- 🧠 Reflection: Successfully integrated research agent output with manual planning. Resolved research.md duplication by merging comprehensive agent research (56KB) with decision summary table. All planning artifacts follow Spec-Kit Plus conventions and provide clear implementation guidance.

## Evaluation notes (flywheel)

- Failure modes observed: Research agent created research.md at project root instead of feature directory (fixed by moving and merging)
- Graders run and results (PASS/FAIL): Constitution Check - PASS (7/7 principles), Research quality - PASS (comprehensive with references)
- Prompt variant (if applicable): Standard /sp.plan workflow with detailed user requirements
- Next experiment (smallest change to try): Proceed to task generation with /sp.tasks to break down implementation into actionable steps
