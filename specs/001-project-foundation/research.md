# Research: Project Foundation & Architecture

**Feature**: 001-project-foundation
**Date**: 2026-02-02
**Purpose**: Research technical decisions and best practices for project foundation

## Overview

This document captures research findings for establishing the Phase II Todo Application foundation including directory structure, configuration strategy, Docker Compose setup, JWT authentication patterns, and documentation architecture.

## Research Areas

### 1. Monorepo Structure for Full-Stack Applications

**Question**: What is the optimal monorepo structure for a Next.js + FastAPI application?

**Research Findings**:

**Option A: Flat Structure** (frontend/, backend/ at root)
- ✅ Simple navigation
- ✅ Clear separation of concerns
- ✅ Easy for agents to locate components
- ❌ No workspace orchestration tools

**Option B: Packages Structure** (packages/frontend, packages/backend)
- ✅ Supports monorepo tools (Nx, Turborepo)
- ✅ Better for shared libraries
- ❌ Additional complexity for simple project
- ❌ Overhead not justified for 2 services

**Decision**: **Flat Structure (Option A)**

**Rationale**:
- Project has only 2 services (frontend, backend)
- No shared code libraries between TypeScript and Python
- Agent instructions easier with flat paths
- Aligns with 2-hour timeline constraint (no monorepo tool setup)
- Supports independent deployment if needed

**Alternatives Considered**:
- Turborepo monorepo: Rejected due to setup complexity and limited benefit for Python/TypeScript split
- Nx workspace: Rejected due to learning curve and unnecessary for this scale

---

### 2. Docker Compose Configuration Strategy

**Question**: How should Docker Compose be configured for local development with Next.js, FastAPI, and external Neon PostgreSQL?

**Research Findings**:

**Option A: All Services in Docker** (frontend, backend, local PostgreSQL)
- ✅ Complete environment isolation
- ✅ Consistent across machines
- ❌ Slow hot reload for Next.js in Docker
- ❌ Requires local PostgreSQL (conflicts with Neon requirement)

**Option B: Frontend and Backend in Docker, External Database**
- ✅ Fast Next.js hot reload
- ✅ Uses Neon PostgreSQL (no local DB)
- ✅ Simpler Docker Compose configuration
- ✅ Matches production architecture
- ❌ Requires Neon connection string in .env

**Option C: Native Development** (no Docker Compose)
- ✅ Fastest development iteration
- ❌ Environment inconsistencies
- ❌ Manual service management
- ❌ Violates FR-007 (Docker Compose requirement)

**Decision**: **Option B - Frontend and Backend in Docker, External Database**

**Rationale**:
- Meets FR-007 requirement (Docker Compose for services)
- Aligns with Neon PostgreSQL constraint (no local database)
- Fast hot reload for both services (volume mounts)
- Simplified configuration (2 services vs 3)
- Production-like environment (external managed database)

**Configuration Pattern**:
```yaml
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    volumes: ["./frontend:/app"]
    environment:
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - NEXT_PUBLIC_API_URL=http://backend:8000

  backend:
    build: ./backend
    ports: ["8000:8000"]
    volumes: ["./backend:/app"]
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - CORS_ORIGINS=http://localhost:3000
```

---

### 3. Environment Variable Management

**Question**: Should environment variables be in a single root .env file or separate .env files per service?

**Research Findings**:

**Option A: Single Root .env File**
- ✅ Single source of truth
- ✅ Easier to verify BETTER_AUTH_SECRET matches
- ✅ Docker Compose reads from root by default
- ❌ Contains variables for multiple services

**Option B: Service-Specific .env Files** (frontend/.env, backend/.env)
- ✅ Service isolation
- ✅ Only relevant variables per service
- ❌ BETTER_AUTH_SECRET duplication risk
- ❌ Docker Compose needs multiple env_file declarations

**Option C: Hybrid Approach** (shared .env + service .env.local)
- ✅ Shared secrets in root
- ✅ Service-specific overrides possible
- ❌ Complexity for simple project
- ❌ Confusion about precedence

**Decision**: **Option A - Single Root .env File** (with service .env.example for documentation)

**Rationale**:
- Docker Compose naturally reads root .env
- Reduces risk of BETTER_AUTH_SECRET mismatch (FR-006 critical requirement)
- Simpler mental model for developers
- Service .env.example files document what each service needs
- Developers copy root .env.example to .env and fill once

**Structure**:
```
# Root .env (actual secrets - gitignored)
BETTER_AUTH_SECRET=...
DATABASE_URL=postgresql://...
NODE_ENV=development

# frontend/.env.example (documentation)
BETTER_AUTH_SECRET=your-secret-here
NEXT_PUBLIC_API_URL=http://localhost:8000

# backend/.env.example (documentation)
BETTER_AUTH_SECRET=your-secret-here
DATABASE_URL=postgresql://user:pass@host/db
CORS_ORIGINS=http://localhost:3000
```

---

### 4. Next.js 16 Breaking Changes

**Question**: What are the critical Next.js 16 breaking changes that must be documented?

**Research Findings**:

**Key Breaking Changes**:

1. **Async Route Params** (CRITICAL)
   - Next.js 15: `params` is synchronous object
   - Next.js 16: `params` is async and must be awaited
   - Impact: All dynamic routes must use `const params = await props.params`

2. **Middleware → Proxy Pattern** (CRITICAL)
   - Next.js 15: Middleware could modify requests
   - Next.js 16: API routes preferred for proxying
   - Impact: Use `/app/api/proxy.ts` not middleware for JWT forwarding

3. **Server Component by Default**
   - All components are Server Components unless 'use client'
   - Client components must explicitly declare

4. **Route Handlers Must Export HTTP Methods**
   - Must export GET, POST, PUT, DELETE, PATCH functions
   - No default export

**Decision**: **Document all four changes in frontend/CLAUDE.md with code examples**

**Rationale**:
- Async params affects every dynamic route (critical for tasks/{id})
- Proxy pattern required for JWT httpOnly cookie forwarding (FR-018)
- Server/Client component distinction affects Better Auth integration
- Route handler pattern required for API proxy implementation

**Documentation Pattern** (for frontend/CLAUDE.md):
```typescript
// ❌ INCORRECT - Next.js 15 pattern
export default function Page({ params }: { params: { id: string } }) {
  return <div>Task {params.id}</div>
}

// ✅ CORRECT - Next.js 16 pattern
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  return <div>Task {id}</div>
}
```

---

### 5. JWT Authentication Flow with httpOnly Cookies

**Question**: How should JWT tokens flow from Better Auth (frontend) to FastAPI (backend) using httpOnly cookies?

**Research Findings**:

**Flow Architecture**:

```
1. User Login
   User → Frontend (Better Auth) → Creates JWT → Sets httpOnly cookie

2. API Request
   Frontend → Next.js API Proxy (/api/proxy.ts)
   - Proxy reads httpOnly cookie (server-side)
   - Forwards request to FastAPI with Authorization header
   - Returns FastAPI response to frontend

3. Backend Verification
   FastAPI Middleware → Extracts JWT from Authorization header
   → Verifies signature using BETTER_AUTH_SECRET
   → Decodes user_id and email
   → Attaches to request.state.user
   → Routes access request.state.user for filtering
```

**Key Patterns**:

**Next.js API Proxy** (`/app/api/proxy.ts`):
```typescript
// Server-side API route that can read httpOnly cookies
export async function POST(request: Request) {
  const cookies = request.headers.get('cookie')
  const jwt = extractJwtFromCookies(cookies) // Read httpOnly cookie

  const response = await fetch(`${BACKEND_URL}${pathname}`, {
    headers: {
      'Authorization': `Bearer ${jwt}`,
      'Content-Type': 'application/json'
    },
    body: await request.text()
  })

  return response
}
```

**FastAPI JWT Middleware** (`middleware/jwt_auth.py`):
```python
from fastapi import Request, HTTPException
from jose import jwt, JWTError

async def verify_jwt(request: Request, call_next):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise HTTPException(401, "Missing authentication")

    token = auth_header.replace('Bearer ', '')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        request.state.user = payload  # Attach user to request
    except JWTError:
        raise HTTPException(401, "Invalid token")

    return await call_next(request)
```

**Decision**: **Use Next.js API Proxy + FastAPI JWT Middleware**

**Rationale**:
- httpOnly cookies secure against XSS (JavaScript cannot access)
- Next.js API routes can read httpOnly cookies server-side
- FastAPI middleware verifies JWT on every request
- User isolation enforced by middleware attaching user to request
- Aligns with FR-010, FR-011, FR-018 requirements

---

### 6. CLAUDE.md Layering Strategy

**Question**: How should agent instructions be organized across root, frontend, and backend CLAUDE.md files?

**Research Findings**:

**Layering Approach**:

**Root CLAUDE.md**:
- Project overview and navigation
- Links to component CLAUDE.md files
- Spec-Driven Development workflow
- PHR creation requirements
- ADR suggestion guidelines
- Constitution principles
- Overall project context

**Frontend CLAUDE.md**:
- Next.js 16 breaking changes and patterns
- Better Auth integration steps
- JWT cookie handling in API proxy
- Component architecture (App Router, Server/Client components)
- Tailwind CSS responsive patterns
- Frontend code standards
- References root CLAUDE.md for workflow

**Backend CLAUDE.md**:
- FastAPI application structure
- SQLModel ORM patterns
- JWT verification middleware
- User isolation enforcement checklist
- Database connection setup
- API endpoint patterns
- Security requirements
- References root CLAUDE.md for workflow

**Decision**: **Three-tier CLAUDE.md structure with clear separation**

**Rationale**:
- Agents need context-specific guidance (frontend agents get frontend patterns)
- Avoids duplication (root holds workflow, components hold tech-specific patterns)
- Enables independent updates (can change frontend patterns without backend impact)
- Meets FR-002, FR-003, FR-004 requirements
- Supports agent specialization (nextjs-frontend-builder, fastapi-backend-builder)

**Cross-References**:
- Component CLAUDE.md links back to root for workflow
- Root CLAUDE.md links forward to components for implementation
- All CLAUDE.md files reference constitution for principles

---

### 7. Spec-Kit Plus Directory Organization

**Question**: What subdirectories should exist under /specs/ following Spec-Kit Plus conventions?

**Research Findings**:

**Standard Spec-Kit Plus Structure**:
```
specs/
├── overview.md          # Project-level documentation
├── architecture.md      # System architecture
├── features/            # Feature specifications
│   └── <feature>.md
├── api/                 # API contracts
│   └── <endpoints>.md
├── database/            # Database schemas
│   └── <schema>.md
└── ui/                  # UI specifications
    └── <components>.md
```

**Decision**: **Follow standard Spec-Kit Plus structure with all four subdirectories**

**Rationale**:
- Meets FR-013 requirement (features/, api/, database/, ui/)
- Separates concerns (features describe behavior, api describes contracts)
- Enables independent evolution (can update API contracts without changing features)
- Supports multi-agent workflow (different agents consume different specs)
- Aligns with existing .specify/ framework structure

**Initial Population**:
- `overview.md`: Project goals, tech stack, core features
- `architecture.md`: System diagram, JWT flow, user isolation
- `features/`: Empty initially (populated by feature specs)
- `api/`: Empty initially (populated by API endpoint specs)
- `database/`: Empty initially (populated by schema specs)
- `ui/`: Empty initially (populated by component specs)

---

### 8. .gitignore Strategy

**Question**: What should be included in .gitignore for this project?

**Research Findings**:

**Essential Ignore Patterns**:

**Environment and Secrets**:
- `.env` (actual secrets)
- `.env.local` (local overrides)
- Keep `.env.example` (templates)

**Dependencies**:
- `node_modules/` (frontend)
- `__pycache__/` (backend)
- `*.pyc` (backend)
- `.next/` (Next.js build)
- `dist/`, `build/` (build artifacts)

**IDE and OS**:
- `.vscode/` (except shared settings)
- `.idea/` (JetBrains)
- `.DS_Store` (macOS)
- `*.swp`, `*.swo` (Vim)

**Temporary Files**:
- `*.log`
- `.pytest_cache/`
- `coverage/`

**Decision**: **Create comprehensive root .gitignore covering all patterns**

**Rationale**:
- Single .gitignore simplifies management
- Covers both frontend (Node.js) and backend (Python) patterns
- Prevents accidental secret commits (critical for BETTER_AUTH_SECRET)
- Reduces repository size (ignores build artifacts and dependencies)

---

## Summary of Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| **Monorepo Structure** | Flat (frontend/, backend/) | Simple, clear separation, agent-friendly |
| **Docker Compose** | Frontend + Backend containers, external DB | Fast reload, Neon PostgreSQL, meets requirements |
| **Environment Variables** | Single root .env + service .env.example | Reduces secret mismatch risk, simpler |
| **Next.js 16 Changes** | Document async params, proxy pattern | Critical for dynamic routes and JWT forwarding |
| **JWT Flow** | Next.js API proxy + FastAPI middleware | Secure httpOnly cookies, user isolation |
| **CLAUDE.md Layering** | Three-tier (root, frontend, backend) | Context-specific, avoids duplication |
| **Spec-Kit Plus Dirs** | features/, api/, database/, ui/ | Standard conventions, separation of concerns |
| **Version Control** | Comprehensive .gitignore | Prevents secret leaks, reduces repo size |

## Implementation Priorities

Based on research findings, implementation should follow this order:

1. **P1 - Directory Structure**: Create all directories (frontend/, backend/, specs/ subdirs)
2. **P1 - Environment Templates**: Create .env.example files with documented variables
3. **P1 - Docker Compose**: Configure services with volume mounts and environment passing
4. **P1 - CLAUDE.md Files**: Write root, frontend, backend agent instructions
5. **P2 - Architecture Docs**: Create specs/architecture.md with JWT flow diagrams
6. **P2 - Overview Doc**: Create specs/overview.md with project description
7. **P2 - README**: Write setup instructions following researched patterns
8. **P3 - .gitignore**: Create comprehensive ignore patterns

## Open Questions

None. All technical decisions resolved through research.

## References

- Next.js 16 Migration Guide: https://nextjs.org/docs/app/building-your-application/upgrading
- Better Auth JWT Documentation: https://better-auth.com/docs/concepts/jwt
- FastAPI Middleware: https://fastapi.tiangolo.com/tutorial/middleware/
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- Spec-Kit Plus Conventions: .specify/templates/spec-template.md
- Docker Compose Best Practices: https://docs.docker.com/compose/compose-file/
