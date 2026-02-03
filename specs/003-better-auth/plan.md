# Implementation Plan: Better Auth Integration with JWT & httpOnly Cookies

**Branch**: `003-better-auth` | **Date**: 2026-02-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-better-auth/spec.md`

## Summary

Implement complete authentication system using Better Auth library on Next.js 16 frontend with JWT tokens stored in httpOnly cookies, integrated with FastAPI backend using JWT verification middleware. System enables user signup, login, logout, session management, and enforces user data isolation through token-based authentication.

**Primary Requirements**:
- User registration and login with email/password
- JWT tokens in httpOnly cookies (7-day expiration)
- Server-side API proxy to forward cookies to backend
- Backend JWT verification middleware
- User ID validation (token vs URL)
- Protected route redirection
- Session persistence across page refreshes

**Technical Approach**:
- Frontend: Better Auth with JWT plugin, Next.js API routes
- Backend: PyJWT verification middleware with FastAPI dependencies
- Cookie flow: httpOnly storage → proxy reads server-side → forwards with Authorization header
- Security: Shared BETTER_AUTH_SECRET, user_id validation, generic error messages

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5+ (Next.js 16)
- Backend: Python 3.11+ (FastAPI)

**Primary Dependencies**:
- Frontend: better-auth (auth library), @better-auth/jwt (JWT plugin), jose (JWT validation)
- Backend: PyJWT or python-jose (JWT verification), python-multipart (form data)

**Storage**:
- PostgreSQL (Neon serverless) with users table
- Session storage: httpOnly cookies (client-side, secure)

**Testing**:
- Frontend: Jest/Vitest with React Testing Library
- Backend: pytest with FastAPI TestClient
- Integration: E2E tests for auth flow

**Target Platform**: Web application (browser + server)

**Project Type**: Web application (frontend + backend)

**Performance Goals**:
- JWT verification: <50ms per request
- Login/signup: <500ms response time
- Session lookup: <10ms (cookie read)

**Constraints**:
- httpOnly cookies only (no localStorage/sessionStorage)
- 7-day token expiration (no refresh tokens)
- BETTER_AUTH_SECRET must match between services
- HTTPS required in production for Secure flag

**Scale/Scope**:
- 1000+ concurrent authenticated users
- 5 auth-related pages (login, signup, logout, protected routes)
- 2 primary workflows (signup → login, login → dashboard)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Principle I: Spec-Driven Development
- **Status**: PASS
- **Evidence**: Specification created at `specs/003-better-auth/spec.md` with 5 user stories, 24 functional requirements, and 10 success criteria
- **Validation**: This plan references and fulfills all spec requirements

### ✅ Principle II: Zero Manual Coding
- **Status**: PASS (by design)
- **Evidence**: All implementation will be via `/sp.tasks` and `/sp.implement` commands
- **Validation**: Plan includes task breakdown structure for agent execution

### ✅ Principle III: User Data Isolation
- **Status**: PASS
- **Evidence**: FR-010 through FR-014 enforce JWT verification and user_id comparison on every request
- **Implementation**: Backend middleware extracts user_id from JWT, compares with URL parameter, rejects mismatches with 403
- **Validation**: User Story 4 (P1) dedicated to testing data isolation

### ✅ Principle IV: JWT-Based Authentication
- **Status**: PASS
- **Evidence**: FR-006 through FR-009, FR-019 require Better Auth with JWT plugin, httpOnly cookies, and shared secret
- **Implementation**: Better Auth issues JWT, stored in httpOnly cookie, proxy forwards to backend, backend verifies with PyJWT
- **Validation**: Matches constitution requirement exactly

### ✅ Principle V: RESTful API Conventions
- **Status**: PASS
- **Evidence**: Authentication endpoints follow REST patterns: POST /api/auth/signup, POST /api/auth/login, POST /api/auth/logout
- **Implementation**: Backend authentication endpoints integrate with existing `/api/{user_id}/tasks` structure
- **Validation**: Consistent with existing task API conventions

### ✅ Principle VI: Responsive Frontend Design
- **Status**: PASS
- **Evidence**: Login and signup forms will use Tailwind CSS with mobile-first approach
- **Implementation**: Forms responsive across mobile (375px), tablet (768px), desktop (1024px+)
- **Validation**: User stories SC-001 and SC-002 measure completion time regardless of device

### ✅ Principle VII: Minimal Viable Product Focus
- **Status**: PASS
- **Evidence**: Out of Scope section excludes password reset, email verification, 2FA, OAuth
- **Implementation**: Focus on core signup, login, logout, session management only
- **Validation**: 5 user stories cover essential authentication without feature creep

**GATE RESULT**: ✅ ALL PRINCIPLES SATISFIED - Proceed to Phase 0 Research

## Project Structure

### Documentation (this feature)

```text
specs/003-better-auth/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0: Better Auth patterns, JWT best practices
├── data-model.md        # Phase 1: User entity and session model
├── quickstart.md        # Phase 1: Setup instructions for auth system
├── contracts/           # Phase 1: API endpoint contracts
│   ├── auth.openapi.yaml
│   └── session.openapi.yaml
└── tasks.md             # Phase 2: /sp.tasks command (NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/                 # ⚠️ SOURCE ROOT (Next.js 16 uses src/)
│   ├── app/             # Next.js App Router
│   │   ├── api/         # API routes (server-side)
│   │   │   ├── auth/    # Better Auth routes
│   │   │   │   └── [...all]/
│   │   │   │       └── route.ts       # Better Auth handler
│   │   │   └── proxy/   # Backend API proxy
│   │   │       └── [...path]/
│   │   │           └── route.ts       # Cookie forwarding proxy
│   │   ├── (auth)/      # Auth route group (public)
│   │   │   ├── login/
│   │   │   │   └── page.tsx           # Login form
│   │   │   └── signup/
│   │   │       └── page.tsx           # Signup form
│   │   ├── (dashboard)/ # Protected route group
│   │   │   └── tasks/
│   │   │       └── page.tsx           # Protected task page
│   │   └── layout.tsx   # Root layout with auth context
│   ├── components/
│   │   ├── auth/        # Auth-specific components
│   │   │   ├── login-form.tsx
│   │   │   ├── signup-form.tsx
│   │   │   └── logout-button.tsx
│   │   └── providers/
│   │       └── auth-provider.tsx      # Session context provider
│   └── lib/
│       ├── auth.ts      # Better Auth configuration
│       └── api-client.ts # API client with proxy calls
├── .env.local           # Frontend environment variables
└── CLAUDE.md

backend/
├── app/                 # ⚠️ APPLICATION ROOT (Python uses app/)
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── jwt.py       # JWT verification middleware
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── auth.py      # FastAPI auth dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py      # User SQLModel (if creating manually)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── auth.py      # Auth request/response schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   └── tasks.py     # Updated with auth middleware
│   └── main.py          # Updated with CORS and middleware
├── .env                 # Backend environment variables
└── CLAUDE.md
```

**Structure Decision**: Web application structure (Option 2) with Next.js frontend and FastAPI backend. Authentication system spans both projects:
- **Frontend**: Better Auth configuration, login/signup pages, API proxy for cookie forwarding
- **Backend**: JWT verification middleware, auth dependencies, protected endpoints
- **Integration**: Shared BETTER_AUTH_SECRET environment variable enables JWT verification across services

## Complexity Tracking

> No violations detected. All complexity is justified by authentication requirements and aligns with constitution principles.
