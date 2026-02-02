---
id: 0003
title: Create Frontend and Backend CLAUDE.md Guidelines
stage: general
date: 2026-02-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: none
labels: ["documentation", "guidelines", "frontend", "backend", "monorepo"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/CLAUDE.md
  - backend/CLAUDE.md
tests:
  - none
---

## Prompt

create frontend and backend CLAUDE.md files write their guidelines and rules in them

## Response snapshot

Created comprehensive CLAUDE.md guidelines for both frontend and backend layers of the monorepo:

### Frontend CLAUDE.md (Next.js 16+)

**Sections created:**
1. **Project Context** - Multi-user todo app with Better Auth and FastAPI backend
2. **Tech Stack** - Next.js 16+, TypeScript, Tailwind CSS, shadcn/ui, Better Auth
3. **Project Structure** - Complete folder organization (app/, components/, lib/, hooks/, types/)
4. **Core Principles:**
   - Server Components by default
   - Authentication flow with JWT httpOnly cookies
   - API communication via centralized client
   - JWT token handling (automatic with credentials: 'include')
5. **Component Patterns** - Client vs Server components with examples
6. **Styling Guidelines** - Tailwind CSS best practices, cn() utility
7. **Error Handling** - API error handling, form validation with Zod
8. **TypeScript Best Practices** - Type definitions, prop types, no any types
9. **Environment Variables** - NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET
10. **File Naming Conventions** - kebab-case, barrel exports
11. **Code Organization** - Colocation, separation of concerns
12. **Performance Guidelines** - Suspense, image optimization, code splitting
13. **Security Best Practices** - XSS prevention, CSRF protection, input validation
14. **Testing Guidelines** - Component testing patterns
15. **Common Patterns** - Loading states, optimistic updates
16. **Development Commands** - npm scripts
17. **Debugging Tips** - React DevTools, Network tab, console logging
18. **Key Reminders** - 10 critical rules to follow

### Backend CLAUDE.md (FastAPI + SQLModel)

**Sections created:**
1. **Project Context** - RESTful API with JWT auth, user isolation, Neon PostgreSQL
2. **Tech Stack** - FastAPI, SQLModel, PostgreSQL, JWT verification, Pydantic
3. **Project Structure** - Complete folder organization (models/, schemas/, routes/, middleware/, dependencies/)
4. **Core Principles:**
   - User isolation (CRITICAL - every query filters by user_id)
   - JWT authentication flow (5-step process)
   - API response format (success/error)
5. **Database Models** - SQLModel Task model with indexes, user_id requirements
6. **Pydantic Schemas** - TaskBase, TaskCreate, TaskUpdate, TaskResponse with validation
7. **API Routes** - Complete CRUD implementation with user isolation for all 6 endpoints:
   - GET /api/{user_id}/tasks
   - POST /api/{user_id}/tasks
   - GET /api/{user_id}/tasks/{id}
   - PUT /api/{user_id}/tasks/{id}
   - DELETE /api/{user_id}/tasks/{id}
   - PATCH /api/{user_id}/tasks/{id}/complete
8. **JWT Authentication** - Middleware implementation, auth dependency
9. **Database Configuration** - Engine setup, connection pooling, settings
10. **Main Application** - FastAPI app with CORS, JWT middleware, lifespan events
11. **Error Handling** - Custom exception handlers, HTTP exceptions with proper status codes
12. **Testing** - Test configuration with in-memory SQLite, test examples
13. **Code Quality Standards** - Type hints (required), docstrings, formatting tools
14. **Security Checklist** - 10 critical security requirements
15. **Performance Guidelines** - Indexed queries, connection pooling, pagination
16. **Development Commands** - Poetry, uvicorn, pytest, type checking, formatting
17. **Debugging Tips** - SQL logging, debugger, request logging
18. **Common Patterns** - Dependency injection, background tasks
19. **Key Reminders** - 10 critical rules to follow

**Key Features of Both Files:**
- Comprehensive coverage of tech stack and patterns
- Security-first approach (user isolation, JWT verification)
- Code examples for all major patterns
- TypeScript/Python type safety emphasized
- Environment variable configuration
- Testing guidelines
- Development workflow commands
- Debugging strategies
- References to project specs

## Outcome

- ✅ Impact: Created comprehensive layer-specific guidelines for frontend (Next.js) and backend (FastAPI) development
- 🧪 Tests: No tests required for documentation
- 📁 Files: Created frontend/CLAUDE.md (600+ lines) and backend/CLAUDE.md (800+ lines)
- 🔁 Next prompts: Create initial project specs in specs/ folder (overview.md, architecture.md, database-schema.md, api-spec.md)
- 🧠 Reflection: Both files provide detailed, actionable guidance with security and best practices emphasized throughout

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (documentation)
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Begin implementing specs using the spec-writer skill or create them manually following Spec-Kit Plus conventions
