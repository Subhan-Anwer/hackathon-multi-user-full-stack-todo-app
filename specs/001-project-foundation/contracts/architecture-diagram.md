# System Architecture Diagram

**Feature**: 001-project-foundation
**Date**: 2026-02-02
**Purpose**: Visual representation of system components and interactions

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                             │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Next.js 16 Frontend (Port 3000)                 │  │
│  │                                                            │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐ │  │
│  │  │   Pages     │  │  Components  │  │  Better Auth    │ │  │
│  │  │ (App Router)│  │   (React)    │  │  (JWT Plugin)   │ │  │
│  │  └─────────────┘  └──────────────┘  └─────────────────┘ │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │          API Proxy (/app/api/proxy.ts)               │ │  │
│  │  │  - Reads httpOnly cookies (server-side)              │ │  │
│  │  │  - Forwards JWT to backend                           │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ HTTP Request
                            │ Authorization: Bearer <JWT>
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (Port 8000)                     │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              JWT Verification Middleware                  │  │
│  │  - Extracts JWT from Authorization header                │  │
│  │  - Verifies signature (BETTER_AUTH_SECRET)               │  │
│  │  - Decodes user_id and email                             │  │
│  │  - Attaches to request.state.user                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Routes                             │  │
│  │  /api/{user_id}/tasks          (GET, POST)              │  │
│  │  /api/{user_id}/tasks/{id}     (GET, PUT, DELETE)       │  │
│  │  /api/{user_id}/tasks/{id}/complete (PATCH)             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │               SQLModel ORM Layer                          │  │
│  │  - User Isolation Enforcement                            │  │
│  │  - WHERE user_id = request.state.user['user_id']        │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ SQL Queries
                            │ (parameterized, user-filtered)
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              Neon PostgreSQL (External Managed)                  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      Tables                               │  │
│  │  - users (id, email, password_hash, created_at)          │  │
│  │  - tasks (id, user_id, title, description, completed)    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### Frontend (Next.js 16)

**Port**: 3000

**Responsibilities**:
- Render user interface (pages, components)
- Handle user authentication via Better Auth
- Store JWT tokens in httpOnly cookies
- Proxy API requests to backend (can't send cookies directly to different origin)
- Manage client-side state and routing

**Key Files**:
- `/app/` - App Router pages and layouts
- `/app/api/proxy.ts` - Server-side API proxy
- `/components/` - React components
- `/lib/auth.ts` - Better Auth configuration
- `/lib/api-client.ts` - Backend API client

**Security**:
- httpOnly cookies protect JWT from XSS attacks
- Server-side API proxy reads cookies (JS cannot)
- CSRF protection via SameSite cookie attribute

---

### Backend (FastAPI)

**Port**: 8000

**Responsibilities**:
- Verify JWT tokens on every request
- Enforce user data isolation
- Execute CRUD operations on tasks
- Interact with database via SQLModel ORM
- Return JSON responses

**Key Files**:
- `main.py` - FastAPI app initialization
- `middleware/jwt_auth.py` - JWT verification
- `routes/tasks.py` - Task CRUD endpoints
- `models.py` - SQLModel database models
- `db.py` - Database connection

**Security**:
- JWT signature verification (BETTER_AUTH_SECRET)
- User ID validation (URL param must match JWT user_id)
- SQL injection prevention (ORM parameterized queries)
- User isolation on all queries (WHERE user_id = ...)

---

### Database (Neon PostgreSQL)

**Location**: External managed service

**Responsibilities**:
- Store user accounts
- Store user tasks
- Enforce referential integrity (foreign keys)
- Provide ACID transactions

**Connection**:
- Via DATABASE_URL environment variable
- SQLModel creates tables automatically (on first run)
- No local database required for development

**Security**:
- Connection string includes credentials (stored in .env)
- TLS encryption for connections (Neon default)
- User data isolated at application level (backend filters queries)

---

## Data Flow Patterns

### Pattern 1: User Registration

```
1. User fills signup form → Frontend
2. Frontend → Better Auth → Creates user account
3. Better Auth → Issues JWT token
4. JWT stored in httpOnly cookie
5. Frontend redirects to dashboard
```

### Pattern 2: User Login

```
1. User submits credentials → Frontend
2. Frontend → Better Auth → Validates credentials
3. Better Auth → Issues JWT token (contains user_id, email, exp)
4. JWT stored in httpOnly cookie
5. Frontend redirects to dashboard
```

### Pattern 3: Authenticated API Request (e.g., Fetch Tasks)

```
1. User visits dashboard → Frontend React component
2. Component → API client → Makes fetch request
3. Request → Next.js API Proxy (/app/api/proxy.ts)
4. Proxy reads httpOnly cookie (server-side)
5. Proxy → Backend (Authorization: Bearer <JWT>)
6. Backend → JWT Middleware → Verifies signature
7. Middleware → Decodes JWT → Attaches user to request
8. Request → Route handler → Validates user_id match
9. Route handler → SQLModel ORM → Query (WHERE user_id = ...)
10. Database → Returns user's tasks
11. Backend → JSON response → Proxy → Frontend
12. Frontend → Renders tasks
```

### Pattern 4: Create Task

```
1. User fills task form → Submit
2. Frontend → API client → POST /api/{user_id}/tasks
3. Request → Next.js API Proxy (with JWT cookie)
4. Proxy → Backend (Authorization: Bearer <JWT>)
5. Backend → JWT Middleware → Verifies and extracts user_id
6. Route handler → Validates user_id (URL) matches JWT user_id
7. Route handler → Creates task (user_id from JWT, not URL)
8. SQLModel → INSERT INTO tasks (user_id, title, ...)
9. Database → Returns created task
10. Backend → JSON response → Frontend
11. Frontend → Updates UI with new task
```

### Pattern 5: Update Task

```
1. User edits task → Submit
2. Frontend → PUT /api/{user_id}/tasks/{task_id}
3. [Same proxy and auth steps as Create Task]
4. Route handler → Fetches existing task (WHERE id = task_id AND user_id = ...)
5. If task not found or wrong user → 404/403 error
6. Route handler → Updates task fields
7. SQLModel → UPDATE tasks SET ... WHERE id = task_id AND user_id = ...
8. Backend → JSON response → Frontend
9. Frontend → Updates UI
```

## Network Communication

### Frontend ↔ Backend

**Protocol**: HTTP/HTTPS
**Format**: JSON request/response bodies
**Authentication**: JWT in Authorization header (proxied from httpOnly cookie)

**Request Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Response Format**:
```json
{
  "data": { ... },      // Success data
  "error": null,        // null on success
  "message": "Success"  // Human-readable message
}
```

**Error Format**:
```json
{
  "data": null,
  "error": "UNAUTHORIZED",
  "message": "Invalid or expired token"
}
```

### Backend ↔ Database

**Protocol**: PostgreSQL wire protocol (over TLS)
**Format**: SQL queries (parameterized via SQLModel)
**Authentication**: Username/password in DATABASE_URL

**Connection String Format**:
```
postgresql://username:password@hostname:port/database?sslmode=require
```

## Security Boundaries

### Boundary 1: Browser → Frontend

**Threats**:
- XSS attacks (malicious scripts)
- CSRF attacks (forged requests)

**Mitigations**:
- httpOnly cookies (JS cannot read JWT)
- SameSite cookie attribute (CSRF protection)
- Content Security Policy headers
- Input sanitization on render

### Boundary 2: Frontend → Backend

**Threats**:
- Token theft (man-in-the-middle)
- Token replay attacks
- Unauthorized API access

**Mitigations**:
- HTTPS in production (TLS encryption)
- JWT expiration (tokens expire after 7 days)
- JWT signature verification (BETTER_AUTH_SECRET)
- CORS restrictions (only allow frontend origin)

### Boundary 3: Backend → Database

**Threats**:
- SQL injection
- Unauthorized data access
- User data leakage

**Mitigations**:
- SQLModel ORM (parameterized queries)
- User isolation enforcement (WHERE user_id = ...)
- TLS encrypted connections
- Database credentials in environment (not code)

## Port Configuration

| Service | Host Port | Container Port | Protocol | Purpose |
|---------|-----------|----------------|----------|---------|
| Frontend | 3000 | 3000 | HTTP | Next.js dev server |
| Backend | 8000 | 8000 | HTTP | FastAPI ASGI server |
| Database | N/A | N/A | PostgreSQL | External (Neon) |

**Port Mapping Notes**:
- Host port = Port on developer's machine
- Container port = Port inside Docker container
- Frontend and backend use identical host and container ports (no translation)
- Database has no local port (external service accessed via internet)

## Environment Variables Flow

```
.env (root, gitignored)
  │
  ├─→ Docker Compose (reads root .env)
  │     │
  │     ├─→ Frontend container (receives BETTER_AUTH_SECRET)
  │     │     └─→ Better Auth uses for JWT signing
  │     │
  │     └─→ Backend container (receives BETTER_AUTH_SECRET, DATABASE_URL)
  │           ├─→ JWT middleware uses for verification
  │           └─→ Database connection uses DATABASE_URL
  │
  └─→ .env.example (template, committed)
        └─→ Documentation for developers
```

**Critical Requirement**: BETTER_AUTH_SECRET must be identical in frontend and backend containers. Docker Compose passes the same value from root .env to both services.

## Deployment View (Development)

```
Developer Machine
│
├─ Docker Engine
│   │
│   ├─ Frontend Container
│   │   ├─ Node.js 18+
│   │   ├─ Next.js 16 app
│   │   └─ Port 3000 exposed
│   │
│   └─ Backend Container
│       ├─ Python 3.9+
│       ├─ FastAPI app
│       └─ Port 8000 exposed
│
└─ Internet Connection
    └─→ Neon PostgreSQL (external)
```

**Volume Mounts**:
- Frontend: `./frontend:/app` (enables hot reload)
- Backend: `./backend:/app` (enables hot reload)

**No Local Database**: Neon PostgreSQL is accessed over the internet. No database container in Docker Compose.

## Error Propagation

```
Database Error
  └─→ SQLModel raises exception
      └─→ FastAPI route handler catches
          └─→ Returns 500 Internal Server Error
              └─→ Frontend displays error message

Authentication Error
  └─→ JWT middleware raises 401 Unauthorized
      └─→ FastAPI returns 401 response
          └─→ Frontend redirects to login

Authorization Error (wrong user)
  └─→ Route handler checks user_id mismatch
      └─→ Returns 403 Forbidden
          └─→ Frontend displays "Access Denied"

Validation Error
  └─→ Pydantic schema validation fails
      └─→ FastAPI returns 422 Unprocessable Entity
          └─→ Frontend displays field errors
```

## Scalability Considerations (Future)

This architecture supports scaling:

**Frontend**:
- Multiple Next.js instances behind load balancer
- Stateless (all state in JWT tokens or database)
- CDN for static assets

**Backend**:
- Multiple FastAPI instances behind load balancer
- Stateless (user context from JWT, no sessions)
- Database connection pooling

**Database**:
- Neon provides automatic scaling
- Read replicas for read-heavy workloads
- Connection pooling via pgbouncer

**Current Scope**: Single instance of each service (development only). Scalability is documented but not implemented in foundation.
