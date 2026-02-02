---
id: 0001
title: Create Hackathon Todo Constitution
stage: constitution
date: 2026-02-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: claude-code
command: /sp.constitution
labels: ["constitution", "governance", "spec-driven", "security", "authentication", "jwt"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (Constitution document, no tests)
---

## Prompt

Create the complete project constitution and setup for Hackathon Phase II: Spec-Driven Full-Stack Todo Application.

PROJECT OVERVIEW:
Build a multi-user web application with persistent storage that transforms a console todo app into a modern full-stack application using spec-driven development with zero manual coding.

TECHNOLOGY STACK:
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT tokens
- Development: Claude Code + Spec-Kit Plus
- Deployment: Docker Compose

REQUIRED FEATURES (Basic Level - All 5 Must Be Implemented):
1. Add Task - Create new todo items
2. Delete Task - Remove tasks from the list
3. Update Task - Modify existing task details
4. View Task List - Display all tasks
5. Mark as Complete - Toggle task completion status

CRITICAL REQUIREMENTS:
- All features must be implemented as a web application
- RESTful API endpoints required
- Responsive frontend interface
- Data stored in Neon PostgreSQL
- User authentication with Better Auth + JWT
- User data isolation (users only see their own tasks)
- Zero manual coding (all generated via agents)

REST API ENDPOINTS REQUIRED:
- GET    /api/{user_id}/tasks           - List all tasks
- POST   /api/{user_id}/tasks           - Create new task
- GET    /api/{user_id}/tasks/{id}      - Get task details
- PUT    /api/{user_id}/tasks/{id}      - Update task
- DELETE /api/{user_id}/tasks/{id}      - Delete task
- PATCH  /api/{user_id}/tasks/{id}/complete - Toggle completion

AUTHENTICATION & SECURITY:
- Better Auth issues JWT tokens on login
- Frontend includes JWT in Authorization header via API proxy
- Backend verifies JWT signature using shared BETTER_AUTH_SECRET
- Backend extracts user_id from JWT and compares with URL parameter
- All database queries filtered by authenticated user_id
- httpOnly cookies used (JavaScript cannot read - requires server-side proxy)

## Response snapshot

Created comprehensive project constitution v1.0.0 with seven core principles:

1. **Spec-Driven Development (NON-NEGOTIABLE)**: All features must originate from specifications before implementation
2. **Zero Manual Coding**: All code generated through Claude Code agents and skills
3. **User Data Isolation (SECURITY CRITICAL)**: Every API endpoint enforces user data boundaries with JWT verification
4. **JWT-Based Authentication**: Better Auth on frontend, httpOnly cookies, verified by FastAPI backend
5. **RESTful API Conventions**: Resource-oriented URLs with standard HTTP methods
6. **Responsive Frontend Design**: Mobile-first, accessible, touch-friendly interfaces
7. **Minimal Viable Product Focus**: Prioritize five core features, avoid over-engineering

Constitution includes:
- **Security Standards**: JWT verification, data protection, error handling, SQL injection prevention
- **Development Workflow**: Six phases from specification to deployment with PHR tracking
- **Governance**: Amendment process, compliance review, ADR guidelines, PHR requirements

All dependent templates (plan-template.md, spec-template.md, tasks-template.md) verified for alignment with constitutional principles.

## Outcome

- ✅ Impact: Project constitution established as authoritative governance document for entire hackathon development workflow
- 🧪 Tests: N/A (governance document)
- 📁 Files: Created .specify/memory/constitution.md (260 lines)
- 🔁 Next prompts: Run `/sp.specify` to create feature specifications for the five core todo features
- 🧠 Reflection: Constitution successfully captures spec-driven workflow, security requirements (JWT + user isolation), and hackathon constraints (MVP focus, zero manual coding)

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution aligns with project requirements
- Graders run and results (PASS/FAIL): Manual review required - constitution covers all specified requirements
- Prompt variant (if applicable): N/A (initial creation)
- Next experiment (smallest change to try): Apply constitution by running `/sp.specify` with first feature (task CRUD operations)
