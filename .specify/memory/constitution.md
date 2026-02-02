<!--
SYNC IMPACT REPORT
===================
Version Change: Initial Creation → 1.0.0
Modified Principles: N/A (Initial constitution)
Added Sections:
  - Core Principles (7 principles)
  - Security Standards
  - Development Workflow
  - Governance
Templates Requiring Updates:
  ✅ plan-template.md - Aligned with constitution principles
  ✅ spec-template.md - Aligned with constitution requirements
  ✅ tasks-template.md - Aligned with constitution task structure
Follow-up TODOs: None
-->

# Hackathon Todo Full-Stack Application Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

Every feature MUST originate from a specification document before any implementation begins. Specifications define **what to build** (user scenarios, requirements, success criteria) and are technology-agnostic. Implementation plans define **how to build** (technical approach, architecture, file structure).

**Rationale**: Ensures clear requirements, prevents scope creep, enables review before coding, and creates documentation-first workflow essential for AI-assisted development.

**Rules**:
- Write specification (`spec.md`) before any code
- Specifications must be user-centric with testable acceptance criteria
- Plans must reference and fulfill all spec requirements
- No implementation without approved spec and plan
- All features tracked in `/specs/<feature-name>/` directory structure

### II. Zero Manual Coding

All code MUST be generated through Claude Code agents and skills. Manual coding is prohibited. Developers act as architects and reviewers, not implementers.

**Rationale**: Validates the agentic development workflow, ensures reproducibility, creates traceable prompt history, and demonstrates true AI-assisted development capabilities.

**Rules**:
- Use `/sp.specify` to create specifications
- Use `/sp.plan` to generate implementation plans
- Use `/sp.tasks` to break down work into actionable tasks
- Use `/sp.implement` to execute task-based implementation
- All agent interactions recorded in Prompt History Records (PHRs)

### III. User Data Isolation (SECURITY CRITICAL)

Every API endpoint MUST enforce user data isolation. Users can only access, modify, or delete their own data. Backend MUST verify JWT tokens and filter all database queries by authenticated user ID.

**Rationale**: Multi-user applications require strict data boundaries. Prevents unauthorized data access, ensures privacy compliance, and maintains trust.

**Rules**:
- All API routes include `{user_id}` path parameter
- Backend extracts `user_id` from verified JWT token
- Backend compares JWT `user_id` with URL parameter (must match)
- All database queries filtered by authenticated user: `WHERE user_id = <authenticated_user_id>`
- Reject requests with 403 Forbidden if user IDs don't match
- No shared or public data access patterns (all data user-scoped)

### IV. JWT-Based Authentication

Authentication MUST use Better Auth on the frontend issuing JWT tokens, stored in httpOnly cookies, and verified by FastAPI backend using shared secret.

**Rationale**: Enables stateless authentication, allows independent verification by frontend and backend, provides automatic token expiry, and avoids session database requirements.

**Rules**:
- Better Auth configured with JWT plugin on Next.js frontend
- JWT tokens stored in httpOnly cookies (JavaScript cannot read)
- Frontend uses server-side API proxy to attach JWT to backend requests
- Backend verifies JWT signature using `BETTER_AUTH_SECRET` environment variable
- Backend middleware extracts user identity from JWT on every request
- Tokens expire automatically (default: 7 days)
- No authentication bypass or token-less endpoints (except public auth endpoints)

### V. RESTful API Conventions

API design MUST follow REST principles with predictable resource-oriented URLs, standard HTTP methods, and consistent response formats.

**Rationale**: Provides intuitive API structure, enables frontend-backend contract clarity, simplifies integration, and follows industry standards.

**Rules**:
- Resource URLs: `/api/{user_id}/tasks`, `/api/{user_id}/tasks/{id}`
- HTTP Methods: GET (read), POST (create), PUT (update), DELETE (remove), PATCH (partial update)
- Response Format: JSON with consistent structure (`{ data, error, message }`)
- Status Codes: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 500 (Server Error)
- All endpoints documented in `/specs/*/contracts/` directory
- Input validation with clear error messages

### VI. Responsive Frontend Design

Frontend interfaces MUST be responsive, accessible, and provide excellent user experience across devices (desktop, tablet, mobile).

**Rationale**: Modern web applications must work on all screen sizes. Ensures broad accessibility and professional appearance.

**Rules**:
- Use Tailwind CSS utility classes for responsive design
- Test layouts at mobile (375px), tablet (768px), and desktop (1024px+) breakpoints
- Implement mobile-first design approach
- Ensure touch-friendly interactive elements (min 44px tap targets)
- Support keyboard navigation and screen readers
- Loading states for async operations
- Error states with user-friendly messages

### VII. Minimal Viable Product Focus

Implementation MUST prioritize the five core features required for Basic Level completion: Add Task, Delete Task, Update Task, View Task List, Mark as Complete.

**Rationale**: Hackathon time constraints require focus on essential functionality. Avoid feature creep and over-engineering.

**Rules**:
- Implement only the required five features first
- No additional features until core five are complete and tested
- Simple, straightforward implementations preferred over complex solutions
- No premature optimization or abstraction
- Single responsibility per component/function
- YAGNI (You Aren't Gonna Need It) principle enforced

## Security Standards

### Authentication & Authorization

- JWT tokens verified on every protected API request
- Tokens contain minimal claims: `user_id`, `email`, `exp`, `iat`
- Shared secret (`BETTER_AUTH_SECRET`) stored in environment variables, never in code
- Frontend and backend must use identical secret for JWT signing/verification
- Token expiration enforced (default 7 days, configurable)
- Refresh token rotation implemented for long-lived sessions

### Data Protection

- All database queries filtered by authenticated user
- No user can access another user's tasks through any endpoint
- SQL injection prevented through ORM (SQLModel) parameterized queries
- Input validation on all user-supplied data (title, description, status)
- Output sanitization for XSS prevention (frontend escapes user content)
- Environment secrets never committed to version control (use `.env` files)

### Error Handling

- Never expose internal error details or stack traces to clients
- Generic error messages for authentication failures (avoid user enumeration)
- Detailed logs server-side for debugging (not exposed to client)
- Rate limiting on authentication endpoints (prevent brute force)

## Development Workflow

### Phase 1: Specification (Required)

1. Run `/sp.specify` with feature description
2. Agent creates `/specs/<feature-name>/spec.md` with:
   - User scenarios and acceptance criteria
   - Functional requirements
   - Success criteria
   - Key entities (data models)
3. Review and approve specification
4. Agent creates Prompt History Record (PHR) in `history/prompts/<feature-name>/`

### Phase 2: Planning (Required)

1. Run `/sp.plan` referencing approved spec
2. Agent generates:
   - `/specs/<feature-name>/plan.md` - Implementation strategy
   - `/specs/<feature-name>/research.md` - Technology research
   - `/specs/<feature-name>/data-model.md` - Database schema
   - `/specs/<feature-name>/contracts/` - API endpoint contracts
3. Review plan for architecture decisions
4. Run `/sp.adr <decision-title>` for significant architectural decisions
5. Agent creates PHR in `history/prompts/<feature-name>/`

### Phase 3: Task Breakdown (Required)

1. Run `/sp.tasks` on approved plan
2. Agent generates `/specs/<feature-name>/tasks.md` with:
   - Setup tasks (project initialization)
   - Foundational tasks (blocking prerequisites)
   - User story tasks (grouped by feature priority)
   - Polish tasks (cross-cutting concerns)
3. Tasks marked with `[P]` for parallel execution
4. Tasks include exact file paths and acceptance criteria
5. Agent creates PHR in `history/prompts/<feature-name>/`

### Phase 4: Implementation (Required)

1. Run `/sp.implement` to execute tasks
2. Agent processes tasks in dependency order
3. Agent marks tasks in progress, then completed
4. Agent commits changes after each logical group
5. Agent creates PHRs for implementation work
6. Run tests after implementation (if specified)

### Phase 5: Integration & Testing

1. Verify all five core features work end-to-end
2. Test authentication flow (signup, login, JWT verification)
3. Test user data isolation (create second user, verify separation)
4. Test responsive design on mobile, tablet, desktop
5. Run integration tests if specified in tasks

### Phase 6: Documentation & Deployment

1. Update README.md with setup instructions
2. Document API endpoints in `/specs/api/`
3. Create deployment guide with Docker Compose instructions
4. Run `/sp.git.commit_pr` to commit and create pull request
5. Create final PHR summarizing completion

## Governance

### Constitution Authority

This constitution supersedes all other development practices, guidelines, or preferences. When conflicts arise between this document and other sources, this constitution takes precedence.

### Amendment Process

1. Amendments require explicit user approval
2. Version number incremented according to:
   - **MAJOR**: Breaking changes to principles or workflow
   - **MINOR**: New principles or substantial additions
   - **PATCH**: Clarifications, typos, non-semantic fixes
3. All amendments documented with rationale
4. Dependent templates updated to maintain consistency
5. Sync Impact Report generated with each amendment

### Compliance Review

- Every specification must align with Core Principles
- Every plan must pass Constitution Check gate
- Every task must reference constitutional requirements
- Agent output must cite this constitution when enforcing rules
- PHRs document adherence to workflow phases

### Architectural Decision Records (ADRs)

Significant architectural decisions MUST be documented when:
1. **Impact**: Decision has long-term consequences (framework, data model, security, platform)
2. **Alternatives**: Multiple viable options were considered
3. **Scope**: Decision is cross-cutting and influences system design

ADRs stored in `history/adr/` with format: `###-decision-title.md`

Agent suggests ADR creation but waits for user approval:
> 📋 Architectural decision detected: [brief description]
> Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

### Prompt History Records (PHRs)

Every user interaction MUST generate a PHR after completion:
- **Constitution stage**: `history/prompts/constitution/`
- **Feature stages**: `history/prompts/<feature-name>/` (spec, plan, tasks, implementation)
- **General**: `history/prompts/general/`

PHRs capture: user input (verbatim), agent response, files modified, stage, date, model, feature context, command, and outcome.

### Runtime Guidance

This constitution provides governance rules. For runtime development guidance (coding patterns, framework specifics, agent instructions), see `/CLAUDE.md` at repository root and subproject levels (`/frontend/CLAUDE.md`, `/backend/CLAUDE.md`).

**Version**: 1.0.0 | **Ratified**: 2026-02-02 | **Last Amended**: 2026-02-02
