# Implementation Plan: Project Foundation & Architecture

**Branch**: `001-project-foundation` | **Date**: 2026-02-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-project-foundation/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Establish complete project foundation for Phase II Todo Application including monorepo directory structure, configuration files, CLAUDE.md agent instructions, Docker Compose orchestration, environment variable templates, and comprehensive architecture documentation. This foundation enables all subsequent feature development by providing clear project structure, development guidelines, and documented system architecture including JWT authentication flow and user data isolation strategy.

**Technical Approach**: Create structured monorepo with separate frontend (Next.js 16+) and backend (FastAPI) directories. Use Docker Compose for service orchestration. Document architecture with visual diagrams showing component interactions and data flow. Provide layered CLAUDE.md files (root, frontend, backend) for agent-specific guidance. Follow Spec-Kit Plus conventions for specs/ directory organization.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.x, Node.js 18+, Next.js 16+
- Backend: Python 3.9+, FastAPI 0.104+
- Configuration: YAML (Docker Compose), Markdown (documentation)

**Primary Dependencies**:
- Frontend: Next.js 16+, Better Auth (JWT plugin), Tailwind CSS
- Backend: FastAPI, SQLModel (ORM), Python-Jose (JWT verification), Uvicorn (ASGI server)
- Database: Neon PostgreSQL (serverless, external)
- DevOps: Docker, Docker Compose

**Storage**:
- Neon PostgreSQL (serverless PostgreSQL, external managed service)
- No local database required for development
- Connection via DATABASE_URL environment variable

**Testing**:
- Not applicable for this foundation feature (no implementation code)
- Configuration validation through Docker Compose startup
- Documentation validation through manual review

**Target Platform**:
- Development: Docker containers on Linux/macOS/Windows with WSL2
- Frontend: Browser (Chrome, Firefox, Safari, Edge)
- Backend: Linux server (Docker container)

**Project Type**: Web application (monorepo with separate frontend and backend)

**Performance Goals**:
- Documentation must be readable and navigable (success criteria SC-001: 2 minutes to identify components)
- Docker Compose startup time under 2 minutes with proper configuration
- README instructions completable within 30 minutes (SC-005)

**Constraints**:
- Timeline: 2 hours to complete all foundation work
- Fixed ports: Frontend 3000, Backend 8000
- BETTER_AUTH_SECRET must match between frontend and backend (critical security requirement)
- Next.js 16 breaking changes must be accommodated (async params, proxy.ts patterns)
- httpOnly cookie strategy required for JWT transmission

**Scale/Scope**:
- Single monorepo project
- 2 services (frontend, backend) + external database
- Approximately 10-15 configuration and documentation files
- Support for 5 basic CRUD operations (Add, Delete, Update, View, Mark Complete)
- Multi-user system with user data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development
✅ **PASS** - This plan implements foundation from approved `spec.md` (001-project-foundation)
- Specification created first with user scenarios and requirements
- Plan references and fulfills all spec requirements (FR-001 through FR-020)
- All deliverables tracked in `/specs/001-project-foundation/` directory

### Principle II: Zero Manual Coding
✅ **PASS** - This is a foundation/configuration feature with no application code
- Deliverables are configuration files, documentation, and directory structure
- Future features will use `/sp.specify`, `/sp.plan`, `/sp.tasks`, `/sp.implement` workflow
- Agent instructions (CLAUDE.md) will guide future agentic development

### Principle III: User Data Isolation
✅ **PASS** - Architecture documentation will specify user isolation strategy
- FR-011: Architecture documentation must explain user data isolation using user_id from JWT
- Backend CLAUDE.md will include security checklist for user isolation enforcement
- All API endpoints documented with `{user_id}` path parameter pattern

### Principle IV: JWT-Based Authentication
✅ **PASS** - Architecture and environment configuration support JWT authentication
- FR-010: Architecture documentation must include JWT authentication flow
- FR-006: Environment variable documentation must state BETTER_AUTH_SECRET must match
- FR-018: Documentation must explain httpOnly cookie strategy
- Docker Compose and .env.example will configure shared secret

### Principle V: RESTful API Conventions
✅ **PASS** - Architecture documentation will establish API conventions
- FR-009: Architecture documentation must document API patterns
- Specs directory includes `/api/` subdirectory for endpoint documentation (FR-013)
- README.md will reference API documentation structure

### Principle VI: Responsive Frontend Design
✅ **PASS** - Frontend CLAUDE.md will establish responsive design requirements
- FR-003: Frontend CLAUDE.md must include architecture patterns
- Documentation will reference Tailwind CSS for responsive utilities
- Mobile-first design approach documented in guidelines

### Principle VII: Minimal Viable Product Focus
✅ **PASS** - Foundation supports five core features without over-engineering
- Documentation scopes project to five basic CRUD operations
- FR-020: Directory structure follows established conventions (no custom complexity)
- Out of scope section explicitly excludes advanced features (CI/CD, production configs)

### Security Standards Compliance
✅ **PASS** - Foundation establishes security requirements
- Authentication & Authorization: JWT verification documented in architecture
- Data Protection: User isolation strategy documented, ORM usage specified
- Error Handling: Documentation will include troubleshooting for common errors

### Workflow Compliance
✅ **PASS** - Following Phase 2 (Planning) of Development Workflow
- Phase 1 (Specification) completed: `spec.md` created and validated
- Currently in Phase 2 (Planning): Creating `plan.md`, will create `research.md`, `data-model.md`, `contracts/`
- Phase 3 (Task Breakdown) next: Will run `/sp.tasks` after plan approval
- PHR will be created after plan completion

### Overall Gate Status
🟢 **ALL CHECKS PASSED** - Proceed to Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/001-project-foundation/
├── spec.md              # Feature specification (already created)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - technology and pattern research
├── data-model.md        # Phase 1 output - configuration entities and structure
├── quickstart.md        # Phase 1 output - developer onboarding guide
├── contracts/           # Phase 1 output - architecture diagrams and flows
│   ├── architecture-diagram.md
│   ├── jwt-flow.md
│   └── directory-structure.md
├── checklists/          # Quality validation checklists
│   └── requirements.md  # Already created - spec validation
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Repository Structure (complete monorepo layout)

```text
hackathon-multi-user-full-stack-todo-app/
├── .specify/                    # Spec-Kit Plus configuration (existing)
│   ├── memory/
│   │   └── constitution.md
│   ├── templates/
│   └── scripts/
│
├── specs/                       # Specification repository (Spec-Kit Plus)
│   ├── 001-project-foundation/  # This feature (current)
│   ├── overview.md              # Project overview documentation (TO CREATE)
│   ├── architecture.md          # System architecture documentation (TO CREATE)
│   ├── features/                # Feature specifications (TO CREATE)
│   ├── api/                     # API endpoint specifications (TO CREATE)
│   ├── database/                # Database schema specifications (TO CREATE)
│   └── ui/                      # UI component specifications (TO CREATE)
│
├── history/                     # Prompt History Records and ADRs (existing)
│   ├── prompts/
│   │   ├── 001-project-foundation/
│   │   ├── constitution/
│   │   └── general/
│   └── adr/
│
├── frontend/                    # Next.js 16+ application (TO CREATE)
│   ├── app/                     # Next.js App Router directory
│   │   ├── (auth)/              # Auth route group
│   │   ├── (dashboard)/         # Protected routes
│   │   ├── api/                 # API proxy routes
│   │   │   └── proxy.ts         # JWT cookie forwarding
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/              # React components
│   │   ├── ui/                  # Reusable UI components
│   │   └── features/            # Feature-specific components
│   ├── lib/                     # Utilities and helpers
│   │   ├── auth.ts              # Better Auth configuration
│   │   ├── api-client.ts        # Backend API client
│   │   └── utils.ts
│   ├── public/                  # Static assets
│   ├── .env.example             # Environment variable template (TO CREATE)
│   ├── next.config.ts           # Next.js configuration
│   ├── tailwind.config.ts       # Tailwind CSS configuration
│   ├── tsconfig.json            # TypeScript configuration
│   ├── package.json             # Dependencies
│   ├── CLAUDE.md                # Frontend agent instructions (TO CREATE)
│   └── README.md                # Frontend setup guide
│
├── backend/                     # FastAPI application (TO CREATE)
│   ├── main.py                  # FastAPI application entry point
│   ├── models.py                # SQLModel database models
│   ├── db.py                    # Database connection and session
│   ├── routes/                  # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication endpoints
│   │   └── tasks.py             # Task CRUD endpoints
│   ├── middleware/              # Custom middleware
│   │   ├── __init__.py
│   │   └── jwt_auth.py          # JWT verification middleware
│   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   └── task.py
│   ├── .env.example             # Environment variable template (TO CREATE)
│   ├── requirements.txt         # Python dependencies
│   ├── CLAUDE.md                # Backend agent instructions (TO CREATE)
│   └── README.md                # Backend setup guide
│
├── .gitignore                   # Git ignore patterns (TO CREATE)
├── docker-compose.yml           # Multi-service orchestration (TO CREATE)
├── CLAUDE.md                    # Root agent instructions (TO UPDATE)
└── README.md                    # Project setup and usage (TO CREATE)
```

**Structure Decision**: **Web Application (Monorepo)**

This project follows a **web application monorepo structure** with separate frontend and backend directories. This decision is based on:

1. **Technology Stack**: Next.js frontend + FastAPI backend require distinct language environments (TypeScript vs Python)
2. **Agent Specialization**: Different AI agents handle frontend (nextjs-frontend-builder) and backend (fastapi-backend-builder), requiring separate instruction files
3. **Deployment Flexibility**: Frontend and backend can be deployed independently while sharing common specifications
4. **Development Workflow**: Developers can work on frontend or backend independently with clear separation of concerns
5. **Spec-Kit Plus Integration**: Centralized `/specs/` directory serves both frontend and backend as single source of truth

**Key Directories**:
- `/specs/`: Centralized specifications following Spec-Kit Plus conventions (shared between frontend/backend)
- `/frontend/`: Next.js 16 App Router structure with Better Auth integration
- `/backend/`: FastAPI structure with SQLModel ORM and JWT middleware
- `/history/`: PHRs and ADRs tracking all architectural decisions and agent interactions
- `.specify/`: Framework configuration and templates (existing)

## Complexity Tracking

**Status**: No violations detected. All constitution checks passed without requiring complexity justification.

This foundation feature maintains minimal complexity:
- Single monorepo (not multiple repositories)
- Direct configuration files (no abstraction layers)
- Standard directory structures following established conventions
- Documentation-only deliverables (no implementation code at this stage)

---

## Phase 0 & Phase 1 Completion Summary

### Phase 0: Research (Completed)

**Output**: `research.md` - 8 research areas with decisions and rationale

**Key Decisions Made**:
1. ✅ Monorepo Structure: Flat structure (frontend/, backend/ at root)
2. ✅ Docker Compose: Frontend + Backend containers, external Neon database
3. ✅ Environment Variables: Single root .env + service .env.example templates
4. ✅ Next.js 16 Changes: Documented async params, proxy pattern, server/client components
5. ✅ JWT Flow: Next.js API proxy + FastAPI middleware pattern
6. ✅ CLAUDE.md Layering: Three-tier (root, frontend, backend) with clear separation
7. ✅ Spec-Kit Plus Dirs: features/, api/, database/, ui/ subdirectories
8. ✅ Version Control: Comprehensive .gitignore for Node.js and Python

**All unknowns resolved** - No NEEDS CLARIFICATION items remaining.

---

### Phase 1: Design & Contracts (Completed)

**Output**: `data-model.md`, `contracts/`, `quickstart.md`

#### data-model.md
Defines configuration entities and structural relationships:
- **ProjectStructure**: Monorepo directory organization
- **EnvironmentConfiguration**: Environment variables with validation rules
- **DockerComposeService**: Service definitions with dependencies
- **AgentInstructions**: CLAUDE.md layering and content structure
- **ArchitectureDocumentation**: System docs (overview.md, architecture.md)
- **SpecificationDirectory**: Spec-Kit Plus subdirectories

Includes entity relationships diagram and validation matrix.

#### contracts/ (Architecture Diagrams and Flows)

**architecture-diagram.md**:
- High-level system architecture (Frontend → Backend → Database)
- Component responsibilities (Next.js, FastAPI, Neon PostgreSQL)
- Data flow patterns (5 patterns documented)
- Network communication protocols
- Security boundaries
- Port configuration
- Environment variable flow
- Deployment view
- Error propagation
- Scalability considerations

**jwt-flow.md**:
- JWT token structure (header, payload, signature)
- 5 complete flows:
  1. User Registration
  2. User Login
  3. Authenticated API Request (detailed 10-step cycle)
  4. Token Expiration and Refresh
  5. User Logout
- Security considerations (5 threats with mitigations)
- Configuration requirements
- Validation checklist
- Testing scenarios
- Implementation file references

**directory-structure.md**:
- Complete directory tree (all files and paths)
- Directory purposes (specification, application)
- File naming conventions
- Access patterns for developers/agents
- Growth patterns (adding features, populating subdirectories)
- Validation rules (structural integrity, file completeness, naming)
- Migration paths
- Quick reference cards
- Troubleshooting guide

#### quickstart.md
Developer onboarding guide:
- Prerequisites (Docker, Git)
- Quick setup (10 minutes)
- Project navigation
- Development workflow
- Authentication understanding
- API endpoints reference
- Common tasks (create page, add endpoint, add env var, install deps)
- Troubleshooting (5 common problems)
- Development tips
- Next steps
- Quick reference card
- Success checklist

---

### Agent Context Update (Completed)

✅ Ran `.specify/scripts/bash/update-agent-context.sh claude`
✅ Updated `CLAUDE.md` with plan context (no language-specific updates needed for foundation feature)

---

### Constitution Check Re-evaluation

**Status**: ✅ ALL CHECKS STILL PASSING

After Phase 1 design, re-confirming constitution compliance:

- ✅ **Spec-Driven Development**: Plan references and fulfills all spec requirements
- ✅ **Zero Manual Coding**: Configuration and documentation only
- ✅ **User Data Isolation**: Strategy documented in jwt-flow.md and architecture-diagram.md
- ✅ **JWT-Based Authentication**: Complete flow documented with security considerations
- ✅ **RESTful API Conventions**: Patterns established in architecture documentation
- ✅ **Responsive Frontend Design**: Guidelines prepared for frontend/CLAUDE.md
- ✅ **Minimal Viable Product**: Foundation supports 5 core features without over-engineering

---

## Next Steps

### Immediate: Phase 2 - Task Breakdown

Run `/sp.tasks` to generate actionable, dependency-ordered tasks.

Expected task categories:
1. **Setup Tasks**: Create directory structure, initialize Git, set up Docker
2. **Foundational Tasks**: Create configuration files (.env.example, docker-compose.yml, .gitignore)
3. **Documentation Tasks**: Create CLAUDE.md files, specs/overview.md, specs/architecture.md, README.md
4. **Validation Tasks**: Verify directory structure, test Docker Compose startup, validate documentation

### After Task Generation

Run `/sp.implement` to execute tasks in dependency order.

### Architectural Decisions Detected

📋 **Potential ADRs** (user approval required):

1. **Monorepo Structure Decision**
   - Decision: Flat structure (frontend/, backend/) vs packages/ workspace
   - Rationale: Simplicity, agent-friendly, no shared libraries
   - Alternatives: Turborepo, Nx workspace (rejected due to complexity)
   - Run: `/sp.adr monorepo-structure-decision`

2. **JWT Authentication Strategy**
   - Decision: httpOnly cookies + Next.js proxy + FastAPI middleware
   - Rationale: Security (XSS protection), stateless authentication
   - Alternatives: Session-based auth, localStorage tokens (rejected due to security)
   - Run: `/sp.adr jwt-authentication-strategy`

3. **External Database Choice**
   - Decision: Neon PostgreSQL (serverless) vs local PostgreSQL container
   - Rationale: No local setup, matches production, faster development
   - Alternatives: Local PostgreSQL, SQLite (rejected for different reasons)
   - Run: `/sp.adr external-database-choice`

**Recommendation**: Document these decisions if user approves, or proceed directly to `/sp.tasks`.

---

## Deliverables Summary

### ✅ Completed

| Artifact | Location | Status |
|----------|----------|--------|
| Implementation Plan | `specs/001-project-foundation/plan.md` | ✅ Complete |
| Research Document | `specs/001-project-foundation/research.md` | ✅ Complete |
| Data Model | `specs/001-project-foundation/data-model.md` | ✅ Complete |
| Architecture Diagram | `specs/001-project-foundation/contracts/architecture-diagram.md` | ✅ Complete |
| JWT Flow | `specs/001-project-foundation/contracts/jwt-flow.md` | ✅ Complete |
| Directory Structure | `specs/001-project-foundation/contracts/directory-structure.md` | ✅ Complete |
| Quickstart Guide | `specs/001-project-foundation/quickstart.md` | ✅ Complete |

### ⏳ Pending (Created by /sp.tasks)

| Artifact | Location | Status |
|----------|----------|--------|
| Task Breakdown | `specs/001-project-foundation/tasks.md` | ⏳ Pending |

### 📋 To Be Created (During Implementation)

| Artifact | Location | Created By |
|----------|----------|------------|
| Root CLAUDE.md | `CLAUDE.md` | Implementation tasks |
| Frontend CLAUDE.md | `frontend/CLAUDE.md` | Implementation tasks |
| Backend CLAUDE.md | `backend/CLAUDE.md` | Implementation tasks |
| Environment Templates | `frontend/.env.example`, `backend/.env.example` | Implementation tasks |
| Docker Compose | `docker-compose.yml` | Implementation tasks |
| Git Ignore | `.gitignore` | Implementation tasks |
| Project Overview | `specs/overview.md` | Implementation tasks |
| System Architecture | `specs/architecture.md` | Implementation tasks |
| README | `README.md` | Implementation tasks |
| Spec Subdirectories | `specs/features/`, `specs/api/`, `specs/database/`, `specs/ui/` | Implementation tasks |

---

## Plan Approval

This implementation plan is ready for review and approval.

**Review Checklist**:
- ✅ All Technical Context fields resolved (no NEEDS CLARIFICATION)
- ✅ Constitution Check passed (all principles compliant)
- ✅ Research completed with decisions documented
- ✅ Data model defines all configuration entities
- ✅ Architecture diagrams show complete system design
- ✅ JWT flow documented with security considerations
- ✅ Directory structure provides complete reference
- ✅ Quickstart guide enables fast developer onboarding
- ✅ Agent context updated

**Approval Actions**:
1. Review this plan document
2. Review all deliverables in `specs/001-project-foundation/`
3. Approve to proceed to Phase 2 (Task Breakdown)
4. Run `/sp.tasks` to generate implementation tasks
