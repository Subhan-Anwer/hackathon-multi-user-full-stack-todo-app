# System Architecture

**Project**: Phase II Todo Application
**Last Updated**: 2026-02-03
**Status**: Foundation Complete

## Table of Contents
1. [System Architecture](#system-architecture-overview)
2. [JWT Authentication Flow](#jwt-authentication-flow)
3. [User Data Isolation](#user-data-isolation-strategy)
4. [Component Interactions](#component-interaction-patterns)
5. [Security Boundaries](#security-boundaries)
6. [Port Configuration](#port-configuration)
7. [Environment Variable Flow](#environment-variable-flow-diagram)

---

## System Architecture Overview

### Multi-Tier Architecture

The application follows a three-tier architecture pattern:

```
┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION TIER                           │
│                   Frontend (Next.js 16)                          │
│                      Port 3000                                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ HTTP/HTTPS
                            │ JWT in Authorization header
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                     APPLICATION TIER                             │
│                    Backend (FastAPI)                             │
│                      Port 8000                                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ SQL Queries
                            │ (user-filtered)
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                       DATA TIER                                  │
│              Neon PostgreSQL (Serverless)                        │
│                   (External Managed)                             │
└─────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### Frontend (Next.js 16 + Better Auth)
**Responsibilities**:
- User interface rendering (React Server + Client Components)
- JWT token management (Better Auth with httpOnly cookies)
- API request proxying (server-side cookie reading)
- Client-side routing (Next.js App Router)
- Form validation and user input handling

**Technology**:
- Next.js 16 (App Router)
- TypeScript
- Tailwind CSS 4
- Better Auth (JWT plugin)
- Radix UI components

**Key Files**:
- `frontend/src/app/` - Pages and route groups
- `frontend/src/components/` - React components
- `frontend/src/lib/auth.ts` - Better Auth configuration
- `frontend/src/app/api/proxy/` - API proxy routes

#### Backend (FastAPI + SQLModel)
**Responsibilities**:
- JWT token verification (middleware)
- Business logic execution
- User data isolation enforcement
- Database operations (SQLModel ORM)
- API endpoint handling (RESTful)

**Technology**:
- FastAPI (Python 3.12+)
- SQLModel (SQLAlchemy + Pydantic)
- Uvicorn (ASGI server)
- Python-Jose (JWT verification)

**Key Files**:
- `backend/app/main.py` - Application entry point
- `backend/app/middleware/auth.py` - JWT verification
- `backend/app/routes/tasks.py` - Task CRUD endpoints
- `backend/app/models/` - Database models

#### Database (Neon PostgreSQL)
**Responsibilities**:
- Persistent data storage
- ACID transaction guarantees
- Referential integrity enforcement
- Query execution and indexing

**Technology**:
- PostgreSQL 15+ (Neon Serverless)
- TLS-encrypted connections
- Automatic backups and point-in-time recovery

**Key Tables**:
- `users` - User accounts (authentication data)
- `tasks` - Todo items (with user_id foreign key)

---

## JWT Authentication Flow

See detailed JWT flow documentation: `specs/001-project-foundation/contracts/jwt-flow.md`

### Token Structure

**JWT Components**:
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user-123",           // User ID
    "email": "user@example.com",
    "exp": 1738560000,            // Expiration (7 days)
    "iat": 1737960000             // Issued at
  },
  "signature": "HMACSHA256(...)"  // Signed with BETTER_AUTH_SECRET
}
```

### Complete Authentication Cycle

#### 1. Login/Signup
```
User → Frontend (Better Auth)
  → Creates JWT token
  → Stores in httpOnly cookie
  → Redirects to dashboard
```

#### 2. Authenticated API Request
```
1. User Action (Frontend)
   └─> API client makes request

2. Next.js API Proxy (Server-Side)
   ├─> Reads httpOnly cookie
   ├─> Extracts JWT token
   └─> Forwards to backend with Authorization header

3. FastAPI Middleware
   ├─> Extracts JWT from Authorization header
   ├─> Verifies signature using BETTER_AUTH_SECRET
   ├─> Decodes payload to get user_id
   └─> Attaches user to request.state

4. Route Handler
   ├─> Validates URL user_id matches JWT user_id
   ├─> Executes business logic
   └─> Queries database with user_id filter

5. Database
   ├─> Executes query: WHERE user_id = '123'
   └─> Returns user-specific data only

6. Response Path
   Backend → Proxy → Frontend → User
```

#### 3. Token Verification Details
```python
# Backend JWT verification (middleware)
from jose import jwt

try:
    payload = jwt.decode(
        token,
        BETTER_AUTH_SECRET,  # Must match frontend
        algorithms=["HS256"]
    )
    user_id = payload.get("sub")
    email = payload.get("email")

    # Attach to request
    request.state.user = {
        "user_id": user_id,
        "email": email
    }
except jwt.ExpiredSignatureError:
    # Token expired - return 401
except jwt.InvalidTokenError:
    # Invalid token - return 401
```

### Token Lifecycle
- **Creation**: Better Auth (frontend) on login/signup
- **Storage**: httpOnly cookie (browser)
- **Transmission**: Authorization header (proxy → backend)
- **Verification**: FastAPI middleware (every request)
- **Expiration**: 7 days (configurable)
- **Destruction**: Logout or expiration

---

## User Data Isolation Strategy

**Critical Security Requirement**: Every user sees ONLY their own data.

### Isolation Enforcement Layers

#### Layer 1: URL Parameter
All task endpoints include `{user_id}` in the URL:
```
/api/{user_id}/tasks
/api/{user_id}/tasks/{task_id}
```

#### Layer 2: JWT Extraction
Backend middleware extracts user_id from JWT token:
```python
# From verified JWT payload
authenticated_user_id = request.state.user["user_id"]
```

#### Layer 3: User ID Validation
Route handler validates URL matches JWT:
```python
# In route handler
if url_user_id != request.state.user["user_id"]:
    raise HTTPException(status_code=403, detail="Forbidden")
```

#### Layer 4: Database Query Filtering
Every database query includes WHERE clause:
```python
# SQLModel query with user isolation
statement = select(Task).where(
    Task.user_id == authenticated_user_id  # CRITICAL
)
tasks = session.exec(statement).all()
```

### Isolation Examples

**✅ Correct Implementation**:
```python
# Get tasks for authenticated user
@router.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Validate user_id
    if user_id != current_user["user_id"]:
        raise HTTPException(403, "Cannot access another user's tasks")

    # Query with user filter
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()

    return tasks
```

**❌ Incorrect Implementation**:
```python
# SECURITY VULNERABILITY - No user isolation!
@router.get("/api/tasks")
async def get_tasks(session: Session = Depends(get_session)):
    # Returns ALL users' tasks
    tasks = session.exec(select(Task)).all()
    return tasks
```

### Data Isolation Checklist
- [ ] URL includes `{user_id}` parameter
- [ ] JWT middleware extracts user_id
- [ ] Route handler validates user_id match
- [ ] Database query filters by user_id
- [ ] No cross-user data access possible
- [ ] Test with multiple users to verify isolation

---

## Component Interaction Patterns

### Request/Response Cycle: Create Task

```
┌─────────┐   1. Submit Form    ┌──────────┐   2. Proxy Request   ┌──────────┐
│ Browser │ ──────────────────> │ Next.js  │ ──────────────────> │ FastAPI  │
│         │                     │ Proxy    │  Auth: Bearer JWT   │ Backend  │
└─────────┘                     └──────────┘                     └────┬─────┘
     │                                │                                │
     │                                │                           3. Verify JWT
     │                                │                           4. Validate user_id
     │                                │                                │
     │                                │                                ▼
     │                                │                          ┌──────────┐
     │                                │                          │ Database │
     │                                │                          │ (Neon)   │
     │                                │                          └────┬─────┘
     │                                │                                │
     │                                │                           5. INSERT task
     │                                │                           6. RETURN task
     │                                │                                │
     │                                │   7. JSON Response              ▼
     │   8. Update UI   ◄────────────────────────────────────────────────
     │
```

**Step-by-Step**:
1. User fills form and submits
2. Next.js API proxy reads httpOnly cookie, forwards JWT
3. FastAPI middleware verifies JWT signature
4. Route handler validates URL user_id matches JWT user_id
5. Database INSERT with user_id from JWT (not URL)
6. Database returns created task
7. Backend returns JSON response
8. Frontend updates UI with new task

### Data Flow Patterns

#### Pattern 1: Fetch Data (GET)
```
User Action → Frontend Component (useEffect)
  → API Client (fetch)
  → Next.js Proxy (read cookie)
  → FastAPI Route (verify & filter)
  → Database (SELECT WHERE user_id = ...)
  → Response → Frontend → Render
```

#### Pattern 2: Create Data (POST)
```
User Action → Form Submit
  → API Client (POST with data)
  → Next.js Proxy (attach JWT)
  → FastAPI Route (validate user)
  → Database (INSERT with user_id)
  → Response → Frontend → Update state
```

#### Pattern 3: Update Data (PUT/PATCH)
```
User Action → Edit Form
  → API Client (PUT with changes)
  → Next.js Proxy (attach JWT)
  → FastAPI Route (fetch + verify ownership)
  → Database (UPDATE WHERE id AND user_id)
  → Response → Frontend → Refresh
```

#### Pattern 4: Delete Data (DELETE)
```
User Action → Delete Confirmation
  → API Client (DELETE request)
  → Next.js Proxy (attach JWT)
  → FastAPI Route (verify ownership)
  → Database (DELETE WHERE id AND user_id)
  → Response → Frontend → Remove from UI
```

---

## Security Boundaries

### Boundary 1: Browser ↔ Frontend

**Threats**:
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Man-in-the-middle attacks

**Mitigations**:
- ✅ httpOnly cookies (JavaScript cannot access JWT)
- ✅ SameSite=Lax cookie attribute (CSRF protection)
- ✅ Content Security Policy headers
- ✅ HTTPS in production (TLS encryption)
- ✅ Input sanitization before rendering

### Boundary 2: Frontend ↔ Backend

**Threats**:
- Token theft or interception
- Token replay attacks
- Unauthorized API access
- Data injection attacks

**Mitigations**:
- ✅ JWT signature verification (HMAC-SHA256)
- ✅ Token expiration (7 days, configurable)
- ✅ HTTPS in production (TLS encryption)
- ✅ CORS restrictions (only allow frontend origin)
- ✅ Input validation (Pydantic schemas)
- ✅ Rate limiting (production consideration)

### Boundary 3: Backend ↔ Database

**Threats**:
- SQL injection
- Unauthorized data access
- User data leakage
- Connection string exposure

**Mitigations**:
- ✅ SQLModel ORM (parameterized queries)
- ✅ User isolation on ALL queries
- ✅ TLS-encrypted connections (Neon default)
- ✅ DATABASE_URL in environment variables
- ✅ Minimum privilege database user
- ✅ Connection pooling and timeouts

### Security Best Practices

1. **Secrets Management**:
   - Store in `.env` files (gitignored)
   - Never hardcode secrets in code
   - Use strong, random secrets (32+ characters)
   - Rotate secrets periodically

2. **Authentication**:
   - Verify JWT signature on every request
   - Check token expiration
   - Validate user_id matches URL parameter
   - Use httpOnly cookies for token storage

3. **Authorization**:
   - Enforce user isolation on all operations
   - Validate resource ownership before modifications
   - Return 403 Forbidden for unauthorized access

4. **Data Protection**:
   - Use TLS/HTTPS in production
   - Encrypt sensitive data at rest
   - Sanitize all user inputs
   - Log security events

---

## Port Configuration

### Development Ports

| Service | Host Port | Container Port | Protocol | Purpose |
|---------|-----------|----------------|----------|---------|
| Frontend | 3000 | 3000 | HTTP | Next.js development server |
| Backend | 8000 | 8000 | HTTP | FastAPI ASGI server (Uvicorn) |
| Database | N/A | N/A | PostgreSQL | External (Neon PostgreSQL) |

**Notes**:
- Host port = Port on developer's machine
- Container port = Port inside Docker container
- Frontend and backend use same port inside and outside containers
- Database is external (Neon) - no local port needed

### Port Configuration Files

**docker-compose.yml**:
```yaml
services:
  frontend:
    ports:
      - "3000:3000"  # host:container

  backend:
    ports:
      - "8000:8000"  # host:container
```

**Environment Variables**:
```bash
# Frontend .env
NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend port

# Backend .env
PORT=8000                                   # Backend listens on 8000
CORS_ORIGINS=http://localhost:3000         # Frontend origin
```

### Port Conflict Resolution

If ports 3000 or 8000 are already in use:

**Option 1: Change docker-compose.yml**
```yaml
services:
  frontend:
    ports:
      - "3001:3000"  # Access at localhost:3001
```

**Option 2: Stop conflicting service**
```bash
# Find process using port
lsof -i :3000        # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill the process
kill -9 <PID>
```

---

## Environment Variable Flow Diagram

### Root .env → Docker Compose → Services

```
┌─────────────────────────────────────────────────────────────┐
│  Root .env (gitignored)                                      │
│  ─────────────────────────────────────────────────────────  │
│  BETTER_AUTH_SECRET=your-secret-here                        │
│  DATABASE_URL=postgresql://...                              │
│  NODE_ENV=development                                        │
│  CORS_ORIGINS=http://localhost:3000                         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ Docker Compose reads root .env
                            │
┌───────────────────────────▼─────────────────────────────────┐
│  docker-compose.yml                                          │
│  ───────────────────────────────────────────────────────    │
│  services:                                                   │
│    frontend:                                                 │
│      environment:                                            │
│        - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}           │
│        - NEXT_PUBLIC_API_URL=http://localhost:8000          │
│    backend:                                                  │
│      environment:                                            │
│        - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}           │
│        - DATABASE_URL=${DATABASE_URL}                       │
│        - CORS_ORIGINS=${CORS_ORIGINS}                       │
└──────────────────┬───────────────────┬──────────────────────┘
                   │                   │
                   ▼                   ▼
    ┌──────────────────────┐ ┌────────────────────────┐
    │  Frontend Container  │ │  Backend Container     │
    │  ──────────────────  │ │  ───────────────────   │
    │  BETTER_AUTH_SECRET  │ │  BETTER_AUTH_SECRET    │
    │  (for JWT signing)   │ │  (for JWT verifying)   │
    │                      │ │  DATABASE_URL          │
    │                      │ │  (for Neon connection) │
    └──────────────────────┘ └────────────────────────┘
```

### Critical Variable: BETTER_AUTH_SECRET

**Must Be Identical in Both Services**:
```
Root .env → Docker Compose → Frontend (signing)
                          → Backend (verifying)
```

**Why It Must Match**:
1. Frontend signs JWT with secret
2. Backend verifies JWT with same secret
3. If secrets differ, ALL authentication fails
4. Mismatch = 401 Unauthorized errors

**Validation**:
```bash
# Verify both containers have same secret
docker-compose exec frontend printenv BETTER_AUTH_SECRET
docker-compose exec backend printenv BETTER_AUTH_SECRET
# Output should be identical
```

### Environment Variable Precedence

```
1. Container Environment (docker-compose.yml)
   ↓ overrides
2. Root .env file
   ↓ overrides
3. Service .env.example (template only, not loaded)
```

**Best Practice**: Use root `.env` as single source of truth, referenced by `docker-compose.yml`.

---

## Deployment Architecture (Future)

### Production Considerations

**Frontend**:
- Deploy to Vercel/Netlify (edge functions + CDN)
- Environment variables via platform UI
- HTTPS automatic (TLS certificates)

**Backend**:
- Deploy to Railway/Fly.io/Cloud Run
- Environment variables via platform secrets
- HTTPS automatic (TLS termination)

**Database**:
- Neon PostgreSQL (already serverless)
- Connection pooling via pgbouncer
- Automatic backups enabled

**Secrets Management**:
- Use platform secret managers
- Rotate BETTER_AUTH_SECRET periodically
- Never commit secrets to repository

---

## Summary

This architecture provides:
- ✅ **Separation of Concerns**: Frontend, backend, database tiers
- ✅ **Stateless Authentication**: JWT tokens with httpOnly cookies
- ✅ **User Data Isolation**: Multi-layer enforcement
- ✅ **Security**: Multiple boundaries with appropriate mitigations
- ✅ **Scalability**: Stateless design enables horizontal scaling
- ✅ **Developer Experience**: Clear ports, environment variables, and documentation

For implementation details, see component-specific CLAUDE.md files and contracts documentation.
