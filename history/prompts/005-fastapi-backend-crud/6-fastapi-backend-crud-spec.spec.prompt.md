---
id: 6
title: "fastapi-backend-crud-spec"
stage: "spec"
date_iso: "2026-02-04"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "fastapi-backend-crud"
branch: "005-fastapi-backend-crud"
user: "user"
command: "sp.specify"
labels: ["spec", "backend", "authentication", "crud"]
links:
  spec: "specs/006-fastapi-backend-crud/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/006-fastapi-backend-crud/spec.md"
  - "specs/006-fastapi-backend-crud/checklists/requirements.md"
tests_yaml: []
---

# PHR: fastapi-backend-crud-spec

## Prompt Text

FastAPI Backend with CRUD Operations & JWT Security

Target outcome: Complete FastAPI backend with all 6 required endpoints, JWT authentication on every route, user data isolation, proper error handling, and CORS configuration.

Primary deliverables:
1. FastAPI application setup (backend/main.py)
2. Task CRUD routes (backend/routes/tasks.py)
3. Request/response schemas (backend/schemas.py)
4. API endpoint specification (specs/api/rest-endpoints.md)
5. All 6 endpoints fully implemented and secured

Success criteria:
- All 6 endpoints work: GET (list/detail), POST, PUT, DELETE, PATCH
- JWT authentication required on all endpoints
- User can only access their own tasks (isolation enforced)
- All responses include proper HTTP status codes
- Request validation with Pydantic models
- Error handling for all edge cases
- CORS configured for frontend access
- Database sessions managed properly

Constraints:
- Framework: FastAPI only
- Use suitable sub agent and skills
- All routes under /api/{user_id}/
- JWT verification on every endpoint
- User isolation mandatory (compare token user_id with URL user_id)
- Return 401 for auth errors, 403 for forbidden, 404 for not found
- CORS must allow credentials

Technical requirements:
- Use dependency injection for database sessions
- Use dependency injection for JWT verification
- Pydantic models for request/response validation
- HTTPException for all errors
- Proper status codes (200, 201, 400, 401, 403, 404, 500)
- Filter all queries by authenticated user_id

Endpoints required:
1. GET /api/{user_id}/tasks - List all tasks (with optional filtering)
2. POST /api/{user_id}/tasks - Create new task
3. GET /api/{user_id}/tasks/{id} - Get single task
4. PUT /api/{user_id}/tasks/{id} - Update task
5. DELETE /api/{user_id}/tasks/{id} - Delete task
6. PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion

Not building:
- Pagination (return all tasks for now)
- Advanced filtering (just completed/pending)
- Rate limiting
- Caching
- Background tasks

## Response Text

Created comprehensive specification for FastAPI backend with CRUD operations and JWT security. The specification includes user scenarios, functional requirements, key entities, and success criteria, all written in a technology-agnostic way to focus on user value and business needs. The specification covers all required functionality while removing implementation-specific details to ensure it remains focused on what users need rather than how it will be implemented.

## Outcome

Specification created successfully at specs/006-fastapi-backend-crud/spec.md with validation checklist at specs/006-fastapi-backend-crud/checklists/requirements.md. The specification is ready for the planning phase and meets all quality criteria.