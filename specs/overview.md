# Phase II Todo Application - Project Overview

**Status**: In Development
**Last Updated**: 2026-02-03
**Version**: 1.0.0

## What We're Building

A **multi-user todo application** with persistent storage, JWT authentication, and complete user data isolation. Users can create accounts, manage their personal tasks, and access their data securely from any device.

## Project Objectives

### Primary Goal
Transform a basic todo concept into a production-ready multi-user web application that demonstrates modern full-stack development practices using Spec-Driven Development methodology.

### Key Objectives
1. **User Authentication**: Secure signup/signin with JWT tokens
2. **Data Persistence**: PostgreSQL database with SQLModel ORM
3. **User Isolation**: Complete separation of user data (zero data leakage)
4. **Modern Stack**: Next.js 16, FastAPI, Neon PostgreSQL, Better Auth
5. **Developer Experience**: Clear documentation, easy setup, reproducible environments

## Core Features (Basic Level)

### 1. Add Task
**Description**: Create new todo items with title and optional description
**User Value**: Capture tasks quickly without losing track of responsibilities

### 2. Delete Task
**Description**: Remove tasks from the list permanently
**User Value**: Clean up completed or irrelevant tasks

### 3. Update Task
**Description**: Modify existing task details (title, description)
**User Value**: Correct mistakes or add more information as tasks evolve

### 4. View Task List
**Description**: Display all user's tasks in an organized list
**User Value**: See all responsibilities at a glance

### 5. Mark as Complete
**Description**: Toggle task completion status (complete ↔ incomplete)
**User Value**: Track progress and identify what's done vs. pending

### 6. Authentication
**Description**: User signup/signin using Better Auth with JWT tokens
**User Value**: Secure account creation and personalized task management

## Tech Stack

### Frontend
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **UI Components**: Radix UI, shadcn/ui
- **Authentication**: Better Auth (JWT plugin)
- **Package Manager**: npm

### Backend
- **Framework**: FastAPI (Python 3.12+)
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Authentication**: JWT verification middleware
- **Validation**: Pydantic schemas
- **ASGI Server**: Uvicorn
- **Package Manager**: uv

### Database
- **Provider**: Neon Serverless PostgreSQL
- **Type**: PostgreSQL (managed, serverless)
- **Connection**: TLS-encrypted connections
- **Management**: SQLModel automatic table creation

### Development Tools
- **Methodology**: Spec-Driven Development (Claude Code + Spec-Kit Plus)
- **Containerization**: Docker & Docker Compose
- **Version Control**: Git
- **Documentation**: Markdown specifications

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │   Next.js 16 Frontend (Port 3000)                   │   │
│  │   - React Server Components                         │   │
│  │   - Better Auth (JWT)                               │   │
│  │   - Tailwind CSS                                    │   │
│  └──────────────────┬──────────────────────────────────┘   │
└────────────────────┼────────────────────────────────────────┘
                     │ HTTP/HTTPS
                     │ Authorization: Bearer <JWT>
                     ▼
┌─────────────────────────────────────────────────────────────┐
│            FastAPI Backend (Port 8000)                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │   JWT Verification Middleware                       │   │
│  │   - Verify signature (BETTER_AUTH_SECRET)           │   │
│  │   - Extract user_id                                 │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     ▼                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │   API Routes (with user isolation)                  │   │
│  │   - /api/{user_id}/tasks (CRUD operations)         │   │
│  └──────────────────┬──────────────────────────────────┘   │
└────────────────────┼────────────────────────────────────────┘
                     │ SQL Queries (user-filtered)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│         Neon PostgreSQL (Serverless)                         │
│  - tasks table (with user_id column)                        │
│  - users table (authentication data)                        │
└─────────────────────────────────────────────────────────────┘
```

### Key Architectural Principles

1. **Separation of Concerns**: Frontend handles UI/UX, backend handles business logic and data
2. **Stateless Authentication**: JWT tokens enable stateless authentication (no session storage)
3. **User Isolation**: Every database query filters by authenticated user_id
4. **API-First Design**: RESTful API with clear contracts
5. **Type Safety**: TypeScript (frontend) + Pydantic (backend) = full stack type safety

## Authentication Approach

### JWT Token Flow (httpOnly Cookies)

1. **User Login** → Better Auth creates JWT token
2. **Token Storage** → Stored in httpOnly cookie (JavaScript cannot access)
3. **API Requests** → Next.js API proxy reads cookie (server-side), forwards JWT to backend
4. **Backend Verification** → FastAPI middleware verifies signature, extracts user_id
5. **Data Filtering** → All database queries filter by user_id from JWT

**Why httpOnly Cookies?**
- **Security**: JavaScript cannot read the cookie (XSS protection)
- **Automatic**: Browser automatically includes cookie in same-origin requests
- **Stateless**: No session storage needed on server

## User Data Isolation Strategy

Every user sees only their own data. This is enforced at multiple levels:

1. **URL Level**: All endpoints include `{user_id}` path parameter
2. **JWT Level**: Backend extracts user_id from verified JWT token
3. **Validation Level**: Backend verifies URL user_id matches JWT user_id
4. **Database Level**: All queries include `WHERE user_id = <authenticated_user_id>`

**Example Query**:
```sql
-- ✅ Correct (user-isolated)
SELECT * FROM tasks WHERE user_id = '123'

-- ❌ Wrong (exposes all users' data)
SELECT * FROM tasks
```

## Development Workflow (Spec-Driven Development)

### Phase 1: Specification
Run `/sp.specify` to create feature specification with user scenarios and requirements.

### Phase 2: Planning
Run `/sp.plan` to generate implementation plan, research decisions, and technical design.

### Phase 3: Task Breakdown
Run `/sp.tasks` to break down plan into actionable, dependency-ordered tasks.

### Phase 4: Implementation
Run `/sp.implement` to execute tasks and build the feature.

### Phase 5: Documentation
All work is documented via Prompt History Records (PHRs) and Architecture Decision Records (ADRs).

## Project Timeline & Scope

### Current Phase
**Phase II**: Multi-User Full-Stack Web Application Foundation
- **Status**: Foundation setup in progress
- **Timeline**: 2-hour foundation sprint
- **Deliverables**: Directory structure, configuration, documentation

### Future Phases
- **Phase II-A**: Feature implementation (task CRUD operations)
- **Phase II-B**: UI/UX polish and responsive design
- **Phase II-C**: Testing and quality assurance
- **Phase II-D**: Deployment and production readiness

### Out of Scope (Not Building)
- Advanced features (tags, filters, sorting, search)
- Real-time collaboration or updates
- Mobile native applications
- CI/CD pipelines or automated deployments
- Production infrastructure or monitoring
- Performance optimization or scaling
- Admin panel or user management UI

## Success Metrics

### Technical Success
- ✅ All 5 core CRUD operations functional
- ✅ JWT authentication working end-to-end
- ✅ Complete user data isolation (zero leakage)
- ✅ Docker Compose starts all services successfully
- ✅ New developers can set up and run within 30 minutes

### User Success
- ✅ Users can create accounts independently
- ✅ Users can manage their tasks without friction
- ✅ Users never see other users' data
- ✅ Application is responsive on mobile, tablet, desktop

### Developer Success
- ✅ Clear specifications guide implementation
- ✅ All architectural decisions documented
- ✅ Component guidelines prevent mistakes
- ✅ Reproducible development environment

## Repository Structure

```
hackathon-multi-user-full-stack-todo-app/
├── specs/                # Requirements and architecture
├── history/              # PHRs and ADRs
├── frontend/             # Next.js 16 app
├── backend/              # FastAPI app
├── .env.example          # Environment variables template
├── docker-compose.yml    # Service orchestration
├── PROJECT_STRUCTURE.md  # Directory structure reference
└── README.md             # Setup and usage guide
```

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Git
- Neon PostgreSQL account (free tier available)

### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd hackathon-multi-user-full-stack-todo-app

# Configure environment
cp .env.example .env
# Edit .env with your BETTER_AUTH_SECRET and DATABASE_URL

# Start services
docker-compose up

# Access application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

See `README.md` for detailed setup instructions.

## Key Documentation

- **Architecture**: `specs/architecture.md` - System design and data flow
- **API Spec**: `specs/api/` - API endpoint contracts
- **Database Schema**: `specs/database/` - Data models and relationships
- **Frontend Guidelines**: `frontend/CLAUDE.md` - Next.js patterns
- **Backend Guidelines**: `backend/CLAUDE.md` - FastAPI patterns
- **Project Structure**: `PROJECT_STRUCTURE.md` - Directory organization

## Questions or Issues?

1. Check `/specs/` for requirements and architecture
2. Review `PROJECT_STRUCTURE.md` for directory organization
3. Consult component `CLAUDE.md` files for implementation guidance
4. Reference `.specify/memory/constitution.md` for project principles

---

**This overview provides the 30,000-foot view. Dive into specific documentation for implementation details.**
