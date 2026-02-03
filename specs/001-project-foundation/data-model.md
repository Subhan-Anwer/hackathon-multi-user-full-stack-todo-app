# Data Model: Project Foundation & Architecture

**Feature**: 001-project-foundation
**Date**: 2026-02-02
**Purpose**: Define configuration entities and structural relationships

## Overview

This data model describes the **configuration entities** and **documentation structures** that comprise the project foundation. Unlike typical data models that define database tables, this model describes the organizational structure of configuration files, documentation, and project artifacts.

## Configuration Entities

### Entity: ProjectStructure

**Purpose**: Represents the complete monorepo directory organization

**Attributes**:
- `root_path`: Absolute path to repository root
- `frontend_dir`: Path to Next.js application (`frontend/`)
- `backend_dir`: Path to FastAPI application (`backend/`)
- `specs_dir`: Path to Spec-Kit Plus specifications (`specs/`)
- `history_dir`: Path to PHRs and ADRs (`history/`)
- `specify_dir`: Path to framework configuration (`.specify/`)

**Relationships**:
- HAS MANY `ComponentDirectory` (frontend, backend)
- HAS MANY `SpecificationDirectory` (features, api, database, ui)
- HAS ONE `RootConfiguration` (docker-compose.yml, .gitignore, README.md)

**Validation Rules**:
- All directories must exist before agent implementation begins
- Directory names must match Spec-Kit Plus conventions
- Frontend and backend must be separate directories (not nested)

**State**: Static (created once during foundation setup)

---

### Entity: EnvironmentConfiguration

**Purpose**: Represents environment variables required for services

**Attributes**:
- `service_name`: Service identifier (frontend, backend, or shared)
- `variable_name`: Environment variable key
- `variable_description`: Human-readable description
- `is_required`: Boolean indicating if variable is mandatory
- `is_secret`: Boolean indicating if value should be in .env (not .env.example)
- `default_value`: Default value if applicable (null for secrets)
- `validation_pattern`: Regex pattern for value validation (optional)

**Relationships**:
- BELONGS TO `ComponentDirectory` (frontend or backend)
- SHARED ACROSS services if `service_name` is "shared"

**Key Variables**:

**Shared Variables** (must match):
- `BETTER_AUTH_SECRET`: JWT signing/verification secret (critical)
  - `is_required`: true
  - `is_secret`: true
  - `validation_pattern`: Minimum 32 characters
  - `shared_validation`: Must be identical in frontend and backend

**Frontend Variables**:
- `NEXT_PUBLIC_API_URL`: Backend API base URL
  - `is_required`: true
  - `default_value`: "http://localhost:8000"
- `NODE_ENV`: Environment mode
  - `is_required`: false
  - `default_value`: "development"

**Backend Variables**:
- `DATABASE_URL`: Neon PostgreSQL connection string
  - `is_required`: true
  - `is_secret`: true
  - `validation_pattern`: postgresql://...
- `CORS_ORIGINS`: Allowed frontend origins
  - `is_required`: true
  - `default_value`: "http://localhost:3000"
- `PORT`: Backend server port
  - `is_required`: false
  - `default_value`: "8000"

**Validation Rules**:
- `BETTER_AUTH_SECRET` must match between frontend and backend (FR-006)
- Secret variables must never have values in .env.example (placeholder only)
- Required variables must be documented in .env.example with descriptions

**State**: Documented in .env.example, actual values in .env (gitignored)

---

### Entity: DockerComposeService

**Purpose**: Represents a service definition in docker-compose.yml

**Attributes**:
- `service_name`: Service identifier (frontend, backend)
- `build_context`: Path to Dockerfile directory
- `port_mapping`: Host:container port mapping
- `volume_mounts`: List of volume mount definitions
- `environment_variables`: List of environment variable references
- `depends_on`: List of service dependencies

**Relationships**:
- REFERENCES `ComponentDirectory` for build context
- REFERENCES `EnvironmentConfiguration` for environment variables
- DEPENDS ON other `DockerComposeService` instances (optional)

**Service Definitions**:

**Frontend Service**:
- `service_name`: "frontend"
- `build_context`: "./frontend"
- `port_mapping`: "3000:3000"
- `volume_mounts`: ["./frontend:/app", "/app/node_modules"]
- `environment_variables`: ["BETTER_AUTH_SECRET", "NEXT_PUBLIC_API_URL"]
- `depends_on`: [] (no dependencies)

**Backend Service**:
- `service_name`: "backend"
- `build_context`: "./backend"
- `port_mapping`: "8000:8000"
- `volume_mounts`: ["./backend:/app"]
- `environment_variables`: ["DATABASE_URL", "BETTER_AUTH_SECRET", "CORS_ORIGINS"]
- `depends_on`: [] (uses external Neon database, no local DB service)

**Validation Rules**:
- Port mappings must match documented ports (FR-008: Frontend 3000, Backend 8000)
- Volume mounts must enable hot reload (bind mount source directories)
- Environment variables must be passed through from .env file
- Build contexts must point to valid directories with Dockerfiles

**State**: Defined in docker-compose.yml, instantiated when services start

---

### Entity: AgentInstructions

**Purpose**: Represents CLAUDE.md files providing agent-specific guidance

**Attributes**:
- `location`: Path to CLAUDE.md file (root, frontend, backend)
- `target_audience`: Agent type (general, nextjs-frontend-builder, fastapi-backend-builder)
- `content_sections`: List of documentation sections
- `references`: Links to other documentation (constitution, specs, root CLAUDE.md)

**Relationships**:
- BELONGS TO `ComponentDirectory` (frontend, backend) or root
- REFERENCES `Constitution` for principles
- REFERENCES `SpecificationDirectory` for requirements

**Content Structure**:

**Root CLAUDE.md**:
- Project overview and tech stack
- Navigation to component CLAUDE.md files
- Spec-Driven Development workflow (phases 1-6)
- PHR creation requirements
- ADR suggestion guidelines
- API endpoint reference
- Authentication and security overview
- Development guidelines

**Frontend CLAUDE.md**:
- Next.js 16 breaking changes (async params, proxy pattern)
- Better Auth integration steps
- JWT httpOnly cookie handling
- App Router architecture
- Component patterns (Server/Client components)
- Tailwind CSS responsive patterns
- API client implementation
- Frontend code standards
- Reference to root CLAUDE.md for workflow

**Backend CLAUDE.md**:
- FastAPI application structure
- SQLModel ORM patterns
- JWT verification middleware
- User isolation enforcement checklist
- Database connection setup (Neon PostgreSQL)
- API endpoint implementation patterns
- Security requirements
- Error handling patterns
- Reference to root CLAUDE.md for workflow

**Validation Rules**:
- Component CLAUDE.md must reference root CLAUDE.md (avoid duplication)
- All Next.js 16 breaking changes documented with code examples (FR-016)
- JWT flow documented end-to-end (FR-010)
- User isolation strategy clearly explained (FR-011)
- httpOnly cookie strategy documented (FR-018)

**State**: Static files, updated when patterns or requirements change

---

### Entity: ArchitectureDocumentation

**Purpose**: Represents system architecture documentation

**Attributes**:
- `document_type`: Type of documentation (overview, architecture, diagram)
- `file_path`: Path to documentation file
- `diagram_format`: Format of visual diagrams (Mermaid, ASCII, etc.)
- `content_sections`: List of documentation sections

**Relationships**:
- STORED IN `SpecificationDirectory` (specs/overview.md, specs/architecture.md)
- REFERENCES `EnvironmentConfiguration` for connection details
- REFERENCES `DockerComposeService` for deployment architecture

**Key Documents**:

**specs/overview.md**:
- Project objectives
- Core features (5 CRUD operations)
- Tech stack summary
- User authentication approach
- Development workflow summary

**specs/architecture.md**:
- System architecture diagram (multi-tier: frontend, backend, database)
- JWT authentication flow diagram (login → token → cookie → verification)
- User data isolation strategy
- Component interaction patterns
- Data flow diagrams (request/response cycles)
- Security boundaries
- Port configuration
- CORS configuration

**Validation Rules**:
- Architecture diagram must show all components (FR-009)
- JWT flow must be complete from login to verification (FR-010)
- User isolation strategy must explain user_id filtering (FR-011)
- All diagrams must be visually clear and accurate (SC-007)

**State**: Static documentation, updated when architecture changes

---

### Entity: SpecificationDirectory

**Purpose**: Represents Spec-Kit Plus subdirectories under /specs/

**Attributes**:
- `directory_name`: Subdirectory name (features, api, database, ui)
- `purpose`: What specifications are stored here
- `file_pattern`: Pattern for files in this directory
- `is_populated`: Boolean indicating if directory has content

**Relationships**:
- CONTAINS `SpecificationFile` instances
- BELONGS TO `ProjectStructure`

**Subdirectory Definitions**:

**features/**:
- `purpose`: Feature specifications (what to build, user scenarios)
- `file_pattern`: `<feature-name>.md`
- `is_populated`: false (populated by future feature specs)

**api/**:
- `purpose`: API endpoint contracts (REST endpoints, request/response schemas)
- `file_pattern`: `<endpoint-group>.md` or `rest-endpoints.md`
- `is_populated`: false (populated when API is designed)

**database/**:
- `purpose`: Database schema specifications (tables, relationships, indexes)
- `file_pattern`: `schema.md` or `<model>.md`
- `is_populated`: false (populated when data models are designed)

**ui/**:
- `purpose`: UI component specifications (components, pages, layouts)
- `file_pattern`: `<component-group>.md` or `components.md`
- `is_populated`: false (populated when UI is designed)

**Validation Rules**:
- All four subdirectories must exist (FR-013)
- Directory structure must follow Spec-Kit Plus conventions (FR-020)
- Empty directories acceptable initially (populated by subsequent features)

**State**: Directories created during foundation, files added by future features

---

## Entity Relationships Diagram

```
ProjectStructure
├── HAS MANY ComponentDirectory
│   ├── frontend/
│   │   ├── HAS ONE AgentInstructions (frontend/CLAUDE.md)
│   │   ├── HAS MANY EnvironmentConfiguration (frontend vars)
│   │   └── REFERENCED BY DockerComposeService (frontend service)
│   └── backend/
│       ├── HAS ONE AgentInstructions (backend/CLAUDE.md)
│       ├── HAS MANY EnvironmentConfiguration (backend vars)
│       └── REFERENCED BY DockerComposeService (backend service)
│
├── HAS MANY SpecificationDirectory
│   ├── features/ (empty initially)
│   ├── api/ (empty initially)
│   ├── database/ (empty initially)
│   └── ui/ (empty initially)
│
├── HAS MANY ArchitectureDocumentation
│   ├── specs/overview.md
│   └── specs/architecture.md
│
└── HAS ONE RootConfiguration
    ├── docker-compose.yml (CONTAINS DockerComposeService instances)
    ├── .gitignore
    ├── .env.example (REFERENCES EnvironmentConfiguration)
    ├── README.md
    └── CLAUDE.md (root AgentInstructions)
```

## Validation Matrix

This matrix shows which entities must be validated together to ensure consistency:

| Entity 1 | Entity 2 | Validation Rule |
|----------|----------|----------------|
| EnvironmentConfiguration (BETTER_AUTH_SECRET) | Frontend .env.example | Variable documented |
| EnvironmentConfiguration (BETTER_AUTH_SECRET) | Backend .env.example | Variable documented |
| EnvironmentConfiguration (BETTER_AUTH_SECRET) | AgentInstructions (root) | Matching requirement documented |
| DockerComposeService (frontend) | ComponentDirectory (frontend/) | Build context exists |
| DockerComposeService (backend) | ComponentDirectory (backend/) | Build context exists |
| DockerComposeService (port 3000) | ArchitectureDocumentation | Port documented correctly |
| DockerComposeService (port 8000) | ArchitectureDocumentation | Port documented correctly |
| AgentInstructions (frontend) | ArchitectureDocumentation | JWT flow documented |
| AgentInstructions (backend) | ArchitectureDocumentation | User isolation documented |
| SpecificationDirectory (all four) | ProjectStructure | All directories exist |

## Implementation Notes

### Critical Paths

**Path 1: Environment Variable Consistency**
```
Root .env.example
  → Frontend .env.example (documents BETTER_AUTH_SECRET)
  → Backend .env.example (documents BETTER_AUTH_SECRET)
  → Docker Compose (passes variables to services)
  → AgentInstructions (warns about matching requirement)
```

**Path 2: Port Configuration**
```
Docker Compose (defines 3000:3000, 8000:8000)
  → ArchitectureDocumentation (documents ports)
  → README.md (references ports in setup)
  → AgentInstructions (specifies port usage)
```

**Path 3: JWT Authentication Flow**
```
ArchitectureDocumentation (documents JWT flow)
  → Frontend AgentInstructions (httpOnly cookie handling)
  → Backend AgentInstructions (JWT verification middleware)
  → README.md (authentication setup steps)
```

### Acceptance Criteria

Each entity must meet these criteria to be considered complete:

**ProjectStructure**:
- ✅ All directories exist and are navigable
- ✅ Directory names match spec.md requirements
- ✅ Structure follows Spec-Kit Plus conventions

**EnvironmentConfiguration**:
- ✅ All required variables documented in .env.example
- ✅ BETTER_AUTH_SECRET documented in 2+ locations
- ✅ No actual secrets in .env.example (placeholders only)

**DockerComposeService**:
- ✅ Services start without errors (when .env configured)
- ✅ Ports match documented configuration
- ✅ Hot reload works via volume mounts

**AgentInstructions**:
- ✅ All FR-016, FR-017, FR-018 requirements documented
- ✅ Component CLAUDE.md references root CLAUDE.md
- ✅ Code examples provided for critical patterns

**ArchitectureDocumentation**:
- ✅ Visual diagrams included
- ✅ JWT flow complete from login to verification
- ✅ User isolation strategy explained with user_id filtering

**SpecificationDirectory**:
- ✅ All four subdirectories exist
- ✅ Empty directories acceptable (populated later)
- ✅ Structure matches Spec-Kit Plus conventions

## Change Management

When updating configuration entities:

1. **Identify Affected Entities**: Use validation matrix to find dependencies
2. **Update All Related Files**: Ensure consistency across related entities
3. **Validate Cross-References**: Check that all references remain valid
4. **Update Documentation**: Reflect changes in architecture docs and README
5. **Create PHR**: Document what changed and why

Example: Adding new environment variable
1. Add to EnvironmentConfiguration (this model)
2. Add to appropriate .env.example file
3. Add to Docker Compose environment section
4. Document in README.md setup instructions
5. Update AgentInstructions if pattern-related
6. Create PHR documenting the addition
