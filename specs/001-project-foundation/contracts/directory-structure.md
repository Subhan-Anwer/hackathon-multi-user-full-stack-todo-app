# Directory Structure Reference

**Feature**: 001-project-foundation
**Date**: 2026-02-02
**Purpose**: Complete reference for monorepo organization

## Complete Directory Tree

```
hackathon-multi-user-full-stack-todo-app/
│
├── .specify/                                    # Spec-Kit Plus Framework (existing)
│   ├── memory/
│   │   └── constitution.md                      # Project principles and governance
│   ├── templates/
│   │   ├── spec-template.md                     # Feature specification template
│   │   ├── plan-template.md                     # Implementation plan template
│   │   ├── tasks-template.md                    # Task breakdown template
│   │   └── phr-template.prompt.md               # Prompt History Record template
│   └── scripts/
│       └── bash/
│           ├── create-new-feature.sh            # Initialize feature branch
│           ├── setup-plan.sh                    # Initialize planning workflow
│           ├── create-phr.sh                    # Create Prompt History Record
│           └── update-agent-context.sh          # Update agent-specific files
│
├── specs/                                       # Specification Repository (Spec-Kit Plus)
│   ├── 001-project-foundation/                  # This feature (current)
│   │   ├── spec.md                              # Feature specification
│   │   ├── plan.md                              # Implementation plan
│   │   ├── research.md                          # Technology research
│   │   ├── data-model.md                        # Configuration entities
│   │   ├── quickstart.md                        # Developer onboarding
│   │   ├── contracts/                           # Architecture diagrams
│   │   │   ├── architecture-diagram.md          # System architecture
│   │   │   ├── jwt-flow.md                      # Authentication flow
│   │   │   └── directory-structure.md           # This file
│   │   ├── checklists/                          # Quality validation
│   │   │   └── requirements.md                  # Spec quality checklist
│   │   └── tasks.md                             # Task breakdown (created by /sp.tasks)
│   │
│   ├── overview.md                              # Project overview (TO CREATE)
│   ├── architecture.md                          # System architecture (TO CREATE)
│   │
│   ├── features/                                # Feature specifications (TO CREATE)
│   │   └── (empty initially, populated by future features)
│   │
│   ├── api/                                     # API contracts (TO CREATE)
│   │   └── (empty initially, populated when API is designed)
│   │
│   ├── database/                                # Database schemas (TO CREATE)
│   │   └── (empty initially, populated when models are designed)
│   │
│   └── ui/                                      # UI component specs (TO CREATE)
│       └── (empty initially, populated when UI is designed)
│
├── history/                                     # Historical Records (existing)
│   ├── prompts/                                 # Prompt History Records (PHRs)
│   │   ├── 001-project-foundation/              # Feature-specific PHRs
│   │   │   └── 0001-project-foundation-specification.spec.prompt.md
│   │   ├── constitution/                        # Constitution-related PHRs
│   │   └── general/                             # General purpose PHRs
│   │
│   └── adr/                                     # Architecture Decision Records
│       └── (empty initially, created via /sp.adr)
│
├── frontend/                                    # Next.js 16 Application (TO CREATE)
│   ├── app/                                     # Next.js App Router
│   │   ├── (auth)/                              # Authentication route group
│   │   │   ├── signup/
│   │   │   │   └── page.tsx                     # Signup page
│   │   │   └── signin/
│   │   │       └── page.tsx                     # Signin page
│   │   │
│   │   ├── (dashboard)/                         # Protected routes
│   │   │   ├── tasks/
│   │   │   │   ├── page.tsx                     # Task list page
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx                 # Task detail page
│   │   │   └── layout.tsx                       # Dashboard layout
│   │   │
│   │   ├── api/                                 # API routes (Server-side)
│   │   │   ├── auth/
│   │   │   │   └── [...all]/
│   │   │   │       └── route.ts                 # Better Auth endpoints
│   │   │   └── proxy/
│   │   │       └── [...path]/
│   │   │           └── route.ts                 # Backend API proxy
│   │   │
│   │   ├── layout.tsx                           # Root layout
│   │   └── page.tsx                             # Landing page
│   │
│   ├── components/                              # React Components
│   │   ├── ui/                                  # Reusable UI components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── card.tsx
│   │   │   └── loading.tsx
│   │   │
│   │   └── features/                            # Feature-specific components
│   │       ├── task-list.tsx
│   │       ├── task-item.tsx
│   │       ├── task-form.tsx
│   │       └── auth-form.tsx
│   │
│   ├── lib/                                     # Utilities and Helpers
│   │   ├── auth.ts                              # Better Auth configuration
│   │   ├── api-client.ts                        # Backend API client
│   │   ├── utils.ts                             # Utility functions
│   │   └── types.ts                             # TypeScript type definitions
│   │
│   ├── public/                                  # Static Assets
│   │   ├── favicon.ico
│   │   └── images/
│   │
│   ├── .env.example                             # Environment variable template (TO CREATE)
│   ├── .gitignore                               # Git ignore patterns
│   ├── next.config.ts                           # Next.js configuration
│   ├── tailwind.config.ts                       # Tailwind CSS configuration
│   ├── tsconfig.json                            # TypeScript configuration
│   ├── package.json                             # Node.js dependencies
│   ├── package-lock.json                        # Dependency lock file
│   ├── postcss.config.js                        # PostCSS configuration
│   ├── Dockerfile                               # Docker image definition
│   ├── CLAUDE.md                                # Frontend agent instructions (TO CREATE)
│   └── README.md                                # Frontend setup guide
│
├── backend/                                     # FastAPI Application (TO CREATE)
│   ├── main.py                                  # FastAPI app entry point
│   ├── db.py                                    # Database connection and session
│   ├── models.py                                # SQLModel database models
│   │
│   ├── routes/                                  # API Route Handlers
│   │   ├── __init__.py
│   │   ├── auth.py                              # Authentication endpoints
│   │   └── tasks.py                             # Task CRUD endpoints
│   │
│   ├── middleware/                              # Custom Middleware
│   │   ├── __init__.py
│   │   ├── jwt_auth.py                          # JWT verification middleware
│   │   └── cors.py                              # CORS configuration
│   │
│   ├── schemas/                                 # Pydantic Request/Response Schemas
│   │   ├── __init__.py
│   │   ├── task.py                              # Task schemas
│   │   └── user.py                              # User schemas
│   │
│   ├── services/                                # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── task_service.py                      # Task operations
│   │   └── user_service.py                      # User operations
│   │
│   ├── .env.example                             # Environment variable template (TO CREATE)
│   ├── .gitignore                               # Git ignore patterns
│   ├── requirements.txt                         # Python dependencies
│   ├── Dockerfile                               # Docker image definition
│   ├── CLAUDE.md                                # Backend agent instructions (TO CREATE)
│   └── README.md                                # Backend setup guide
│
├── .gitignore                                   # Root Git ignore patterns (TO CREATE)
├── docker-compose.yml                           # Multi-service orchestration (TO CREATE)
├── CLAUDE.md                                    # Root agent instructions (TO UPDATE)
└── README.md                                    # Project setup and usage (TO CREATE)
```

---

## Directory Purposes

### Specification Directories

**`.specify/`** - Spec-Kit Plus Framework
- **Purpose**: Framework configuration, templates, and automation scripts
- **Owner**: Framework (rarely modified)
- **Key Files**: Constitution, templates, helper scripts

**`specs/`** - Centralized Specifications
- **Purpose**: Single source of truth for all requirements and design
- **Owner**: Product/Architecture team (human or AI)
- **Key Files**: Feature specs, plans, contracts, data models

**`specs/001-project-foundation/`** - This Feature
- **Purpose**: Foundation and architecture deliverables
- **Owner**: This planning phase
- **Key Files**: spec.md, plan.md, research.md, contracts/

**`specs/features/`**, **`specs/api/`**, **`specs/database/`**, **`specs/ui/`**
- **Purpose**: Organized specifications by concern
- **Owner**: Future feature development
- **Status**: Empty initially, populated by subsequent features

**`history/`** - Historical Records
- **Purpose**: Audit trail of decisions and interactions
- **Owner**: Automated (PHRs), manual (ADRs)
- **Key Files**: PHRs per feature, ADRs for major decisions

---

### Application Directories

**`frontend/`** - Next.js 16 Application
- **Purpose**: User-facing web application
- **Language**: TypeScript
- **Framework**: Next.js 16 with App Router
- **Port**: 3000
- **Key Responsibilities**:
  - Render pages and components
  - Handle authentication via Better Auth
  - Store JWT in httpOnly cookies
  - Proxy API requests to backend

**`frontend/app/`** - App Router Structure
- **Purpose**: Next.js 16 routing and pages
- **Conventions**:
  - Route groups: `(auth)/`, `(dashboard)/`
  - Dynamic routes: `[id]/`
  - API routes: `api/*/route.ts`
  - Layouts: `layout.tsx` at each level

**`frontend/components/`** - React Components
- **Purpose**: Reusable UI building blocks
- **Organization**:
  - `ui/` - Generic components (button, input, card)
  - `features/` - Domain-specific components (task-list, auth-form)

**`frontend/lib/`** - Utilities and Configuration
- **Purpose**: Shared logic, helpers, configuration
- **Key Files**:
  - `auth.ts` - Better Auth setup
  - `api-client.ts` - Backend API client
  - `utils.ts` - Utility functions

**`backend/`** - FastAPI Application
- **Purpose**: RESTful API server
- **Language**: Python 3.9+
- **Framework**: FastAPI with SQLModel ORM
- **Port**: 8000
- **Key Responsibilities**:
  - Verify JWT tokens
  - Enforce user data isolation
  - Execute CRUD operations
  - Interact with database

**`backend/routes/`** - API Endpoints
- **Purpose**: HTTP request handlers
- **Organization**: One file per resource (auth.py, tasks.py)
- **Pattern**: RESTful endpoints (GET, POST, PUT, DELETE, PATCH)

**`backend/middleware/`** - Request/Response Interceptors
- **Purpose**: Cross-cutting concerns (auth, CORS, logging)
- **Key Files**:
  - `jwt_auth.py` - JWT verification on every request
  - `cors.py` - CORS policy enforcement

**`backend/schemas/`** - Data Validation
- **Purpose**: Pydantic models for request/response validation
- **Organization**: One file per resource
- **Usage**: Validate input, serialize output

**`backend/services/`** - Business Logic
- **Purpose**: Encapsulate complex operations
- **Organization**: One file per domain (task_service.py, user_service.py)
- **Pattern**: Called by route handlers, uses models/ORM

---

## File Naming Conventions

### Specifications (Markdown)

- **Feature specs**: `specs/###-feature-name/spec.md`
- **Plans**: `specs/###-feature-name/plan.md`
- **Contracts**: `specs/###-feature-name/contracts/<topic>.md`
- **Tasks**: `specs/###-feature-name/tasks.md`
- **PHRs**: `history/prompts/<context>/####-slug.<stage>.prompt.md`
- **ADRs**: `history/adr/####-decision-title.md`

### Frontend (TypeScript/React)

- **Pages**: `page.tsx` (Next.js convention)
- **Layouts**: `layout.tsx` (Next.js convention)
- **API routes**: `route.ts` (Next.js convention)
- **Components**: `kebab-case.tsx` (e.g., `task-list.tsx`)
- **Utilities**: `kebab-case.ts` (e.g., `api-client.ts`)
- **Types**: `types.ts` or `<domain>.types.ts`

### Backend (Python)

- **Main app**: `main.py`
- **Models**: `models.py` or `<model>.py`
- **Routes**: `<resource>.py` (e.g., `tasks.py`)
- **Middleware**: `<purpose>_<type>.py` (e.g., `jwt_auth.py`)
- **Schemas**: `<resource>.py` (e.g., `task.py`)
- **Services**: `<resource>_service.py` (e.g., `task_service.py`)
- **Tests**: `test_<module>.py`

### Configuration

- **Environment templates**: `.env.example` (committed)
- **Actual environment**: `.env` (gitignored)
- **Docker**: `Dockerfile`, `docker-compose.yml`
- **Agent instructions**: `CLAUDE.md` (uppercase)
- **Documentation**: `README.md` (uppercase)

---

## Access Patterns

### Developers/Agents

**Read Specifications**:
1. Start at `specs/###-feature-name/spec.md` (requirements)
2. Review `specs/###-feature-name/plan.md` (approach)
3. Consult `specs/###-feature-name/contracts/` (detailed designs)
4. Check `specs/###-feature-name/tasks.md` (implementation steps)

**Implement Frontend**:
1. Read `frontend/CLAUDE.md` (guidelines)
2. Reference `specs/###-feature-name/contracts/` (API contracts)
3. Create/modify files in `frontend/app/`, `frontend/components/`, `frontend/lib/`
4. Update `frontend/package.json` if dependencies added

**Implement Backend**:
1. Read `backend/CLAUDE.md` (guidelines)
2. Reference `specs/###-feature-name/contracts/` (API contracts, data models)
3. Create/modify files in `backend/routes/`, `backend/models.py`, `backend/middleware/`
4. Update `backend/requirements.txt` if dependencies added

**Record Work**:
1. Run `/sp.phr` to create Prompt History Record
2. Record goes to `history/prompts/###-feature-name/`
3. Run `/sp.adr <decision>` for architectural decisions
4. ADR goes to `history/adr/`

### Configuration Management

**Environment Variables**:
1. Templates in `frontend/.env.example`, `backend/.env.example`
2. Actual values in root `.env` (gitignored)
3. Docker Compose reads root `.env` automatically
4. Services receive values via `environment:` section

**Docker Orchestration**:
1. Root `docker-compose.yml` defines all services
2. Each service has `Dockerfile` in its directory
3. Volume mounts enable hot reload (code changes reflect immediately)
4. Port mappings expose services (3000, 8000)

---

## Growth Patterns

### Adding New Features

```
1. /sp.specify "Feature description"
   → Creates specs/###-new-feature/spec.md

2. /sp.plan
   → Creates specs/###-new-feature/plan.md, research.md, contracts/

3. /sp.tasks
   → Creates specs/###-new-feature/tasks.md

4. /sp.implement
   → Modifies frontend/ and backend/ as needed

5. Commit and merge
   → Feature branch → main branch
```

### Populating Spec Subdirectories

**`specs/features/`**:
- Add when feature has user-facing behavior
- File: `<feature-name>.md`
- Content: User scenarios, acceptance criteria

**`specs/api/`**:
- Add when designing API endpoints
- File: `<endpoint-group>.md` or `rest-endpoints.md`
- Content: OpenAPI schemas, request/response examples

**`specs/database/`**:
- Add when designing data models
- File: `schema.md` or `<model>.md`
- Content: Table definitions, relationships, indexes

**`specs/ui/`**:
- Add when designing components
- File: `<component-group>.md` or `components.md`
- Content: Component specs, props, behavior

---

## Validation Rules

### Structural Integrity

**Rule 1**: Every feature MUST have a directory under `specs/###-feature-name/`
**Rule 2**: Feature directory MUST contain `spec.md` (requirements)
**Rule 3**: If `plan.md` exists, `spec.md` MUST exist first
**Rule 4**: If `tasks.md` exists, `plan.md` MUST exist first
**Rule 5**: Frontend and backend MUST be separate directories (not nested)

### File Completeness

**Rule 6**: Root `.env` MUST contain all variables from frontend and backend `.env.example`
**Rule 7**: `docker-compose.yml` MUST define all services that exist (frontend, backend)
**Rule 8**: Each service directory MUST have `CLAUDE.md` if agents will work there
**Rule 9**: Root `CLAUDE.md` MUST link to component `CLAUDE.md` files

### Naming Consistency

**Rule 10**: Feature directories MUST use pattern `###-kebab-case-name`
**Rule 11**: Feature numbers MUST increment (no gaps, no duplicates)
**Rule 12**: PHR files MUST use pattern `####-slug.<stage>.prompt.md`
**Rule 13**: ADR files MUST use pattern `####-decision-title.md`

---

## Migration Paths

### From Flat to Monorepo

If project started as single directory:

```
Before:
  project/
  ├── frontend files...
  └── backend files...

After:
  project/
  ├── frontend/
  │   └── [moved frontend files]
  └── backend/
      └── [moved backend files]
```

**Steps**:
1. Create `frontend/` and `backend/` directories
2. Move files to appropriate directories
3. Update import paths and references
4. Update `docker-compose.yml` build contexts
5. Update `.gitignore` paths

### Adding Spec-Kit Plus

If project exists without Spec-Kit Plus:

```
1. Copy .specify/ directory structure
2. Create specs/ directory with subdirectories
3. Create history/ directory for PHRs and ADRs
4. Backfill specifications for existing features
5. Update CLAUDE.md to reference Spec-Driven Development workflow
```

---

## Quick Reference

### Most Frequently Accessed Files

**Specifications** (reading requirements):
- `specs/###-feature-name/spec.md`
- `specs/###-feature-name/contracts/`

**Agent Instructions** (coding guidelines):
- `CLAUDE.md` (root)
- `frontend/CLAUDE.md`
- `backend/CLAUDE.md`

**Configuration** (setup):
- `.env.example` (templates)
- `docker-compose.yml` (services)
- `README.md` (instructions)

**Constitution** (principles):
- `.specify/memory/constitution.md`

### Most Frequently Modified Files

**During Feature Development**:
- `frontend/app/**/*.tsx` (pages)
- `frontend/components/**/*.tsx` (components)
- `backend/routes/**/*.py` (endpoints)
- `backend/models.py` (database models)

**During Configuration**:
- `.env` (secrets, connection strings)
- `docker-compose.yml` (service definitions)
- `frontend/.env.example` (template updates)
- `backend/.env.example` (template updates)

### Files Never Modified Manually

- `node_modules/` (managed by npm)
- `__pycache__/` (managed by Python)
- `.next/` (managed by Next.js build)
- `package-lock.json` (managed by npm)

---

## Troubleshooting

**Problem**: Can't find where to add new component

**Solution**: Check file purpose
- Generic UI component? → `frontend/components/ui/`
- Feature-specific component? → `frontend/components/features/`
- Page component? → `frontend/app/<route>/page.tsx`

**Problem**: Environment variable not working

**Solution**: Check configuration chain
1. Is it in root `.env`?
2. Is it referenced in `docker-compose.yml` service environment?
3. Is it documented in `frontend/.env.example` or `backend/.env.example`?
4. Is service restarted after `.env` change?

**Problem**: New feature doesn't have spec

**Solution**: Run Spec-Driven Development workflow
1. `/sp.specify "Feature description"`
2. Review and approve spec
3. `/sp.plan` to design implementation
4. `/sp.tasks` to break down work
5. `/sp.implement` to execute tasks

**Problem**: Can't determine where documentation belongs

**Solution**: Use routing rules
- Project-wide architecture? → `specs/architecture.md`
- Feature requirements? → `specs/###-feature-name/spec.md`
- API contract? → `specs/api/` or `specs/###-feature-name/contracts/`
- Setup instructions? → `README.md`
- Agent guidelines? → `CLAUDE.md` (root, frontend, or backend)
