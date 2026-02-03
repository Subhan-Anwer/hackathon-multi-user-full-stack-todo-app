# Quickstart Guide: Phase II Todo Application

**Feature**: 001-project-foundation
**Date**: 2026-02-02
**Purpose**: Fast-track developer onboarding and environment setup

## What You're Building

A multi-user todo application with:
- **Frontend**: Next.js 16 with Better Auth (JWT authentication)
- **Backend**: FastAPI with SQLModel ORM
- **Database**: Neon PostgreSQL (serverless, no local setup)
- **Security**: JWT tokens in httpOnly cookies, user data isolation

**Core Features**: Add, Delete, Update, View, Mark Complete (5 CRUD operations)

---

## Prerequisites (5 minutes)

### Required Tools

✅ **Docker & Docker Compose**
```bash
# Verify Docker installation
docker --version  # Should be 20.10+
docker compose version  # Should be 2.0+
```

✅ **Git**
```bash
git --version  # Any recent version
```

✅ **Text Editor/IDE**
- VS Code (recommended)
- Any editor with TypeScript and Python support

### Optional (for local development without Docker)

- Node.js 18+ and npm
- Python 3.9+ and pip

---

## Quick Setup (10 minutes)

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd hackathon-multi-user-full-stack-todo-app
```

### Step 2: Create Environment File

```bash
# Copy the example environment file
cp .env.example .env
```

**Edit `.env` and fill in:**

```bash
# CRITICAL: This secret MUST be the same for frontend and backend
BETTER_AUTH_SECRET=your-super-secret-key-at-least-32-characters-long

# Get this from Neon PostgreSQL dashboard (https://neon.tech)
DATABASE_URL=postgresql://username:password@hostname/database?sslmode=require

# Development configuration (defaults)
NODE_ENV=development
NEXT_PUBLIC_API_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000
```

**🚨 CRITICAL**: `BETTER_AUTH_SECRET` must match between frontend and backend. Docker Compose passes the same value from root `.env` to both services.

### Step 3: Get Neon PostgreSQL Database

1. Visit https://neon.tech and sign up (free tier available)
2. Create a new project
3. Copy the connection string (looks like `postgresql://username:password@hostname/database`)
4. Paste into `.env` as `DATABASE_URL`

### Step 4: Start Services

```bash
# Start all services (frontend + backend)
docker compose up

# Or run in background
docker compose up -d
```

**Wait for services to start** (30-60 seconds):
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs

### Step 5: Verify Setup

Open your browser:

1. **Frontend**: http://localhost:3000 (should load landing page)
2. **Backend API Docs**: http://localhost:8000/docs (should show interactive API documentation)
3. **Backend Health Check**: http://localhost:8000/health (should return `{"status": "healthy"}`)

---

## Project Navigation (2 minutes)

### Key Directories

```
hackathon-multi-user-full-stack-todo-app/
├── specs/                    # 📋 Requirements and architecture
│   ├── overview.md           # Start here for project overview
│   ├── architecture.md       # System design and data flow
│   └── 001-project-foundation/  # This feature's documentation
│
├── frontend/                 # ⚛️ Next.js application (port 3000)
│   ├── app/                  # Pages and routes
│   ├── components/           # React components
│   ├── lib/                  # Utilities and API client
│   └── CLAUDE.md             # Frontend development guidelines
│
├── backend/                  # 🐍 FastAPI application (port 8000)
│   ├── main.py               # App entry point
│   ├── routes/               # API endpoints
│   ├── models.py             # Database models
│   ├── middleware/           # JWT authentication
│   └── CLAUDE.md             # Backend development guidelines
│
├── .env                      # 🔐 Secrets (gitignored, you created this)
├── docker-compose.yml        # 🐳 Service orchestration
└── README.md                 # 📖 Detailed setup instructions
```

### Navigation Workflow

**To understand the project**:
1. Read `specs/overview.md` (what we're building)
2. Read `specs/architecture.md` (how it's designed)
3. Review `specs/001-project-foundation/contracts/` (detailed diagrams)

**To develop frontend**:
1. Read `frontend/CLAUDE.md` (guidelines)
2. Code in `frontend/app/`, `frontend/components/`, `frontend/lib/`
3. Reference `specs/001-project-foundation/contracts/jwt-flow.md` for auth patterns

**To develop backend**:
1. Read `backend/CLAUDE.md` (guidelines)
2. Code in `backend/routes/`, `backend/models.py`, `backend/middleware/`
3. Reference `specs/001-project-foundation/contracts/architecture-diagram.md` for system design

---

## Development Workflow

### Making Changes (Hot Reload Enabled)

**Frontend changes**:
```bash
# Edit files in frontend/
# Changes auto-reload in browser (Fast Refresh)
```

**Backend changes**:
```bash
# Edit files in backend/
# Changes auto-reload (Uvicorn reload)
```

**No restart needed!** Volume mounts enable hot reload for both services.

### Running Commands Inside Containers

**Frontend container**:
```bash
# Install new npm package
docker compose exec frontend npm install <package>

# Run frontend tests
docker compose exec frontend npm test

# Access shell
docker compose exec frontend sh
```

**Backend container**:
```bash
# Install new Python package
docker compose exec backend pip install <package>
# Then update backend/requirements.txt

# Run backend tests
docker compose exec backend pytest

# Access shell
docker compose exec backend bash
```

### Viewing Logs

```bash
# All services
docker compose logs -f

# Frontend only
docker compose logs -f frontend

# Backend only
docker compose logs -f backend

# Last 50 lines
docker compose logs --tail 50
```

### Stopping Services

```bash
# Stop all services (keeps containers)
docker compose stop

# Stop and remove containers
docker compose down

# Stop and remove everything (including volumes)
docker compose down -v
```

---

## Understanding Authentication (5 minutes)

### JWT Token Flow

```
1. User signs up/logs in → Frontend (Better Auth)
2. Better Auth creates JWT token with user_id
3. JWT stored in httpOnly cookie (JavaScript cannot read)
4. User makes API request → Next.js API proxy reads cookie
5. Proxy forwards JWT to Backend (Authorization header)
6. Backend verifies JWT signature using BETTER_AUTH_SECRET
7. Backend extracts user_id from JWT
8. Backend filters database query: WHERE user_id = <from_jwt>
9. User only sees their own data
```

**Key Security Points**:
- JWT tokens are signed with `BETTER_AUTH_SECRET`
- httpOnly cookies protect against XSS attacks
- Backend verifies every request
- User data isolation enforced on all queries

**Deep Dive**: Read `specs/001-project-foundation/contracts/jwt-flow.md` for complete flow diagrams.

---

## API Endpoints Reference

All endpoints require JWT authentication (except `/api/auth/*`).

### Authentication

```bash
POST /api/auth/signup     # Create new account
POST /api/auth/signin     # Log in
POST /api/auth/signout    # Log out
```

### Tasks (Protected)

```bash
GET    /api/{user_id}/tasks              # List all user's tasks
POST   /api/{user_id}/tasks              # Create new task
GET    /api/{user_id}/tasks/{id}         # Get task details
PUT    /api/{user_id}/tasks/{id}         # Update task
DELETE /api/{user_id}/tasks/{id}         # Delete task
PATCH  /api/{user_id}/tasks/{id}/complete  # Toggle completion
```

**Interactive API Docs**: http://localhost:8000/docs (Swagger UI)

---

## Common Tasks

### Task 1: Create a New Page

**Frontend** (`frontend/app/about/page.tsx`):
```typescript
export default function AboutPage() {
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold">About</h1>
      <p>This is a multi-user todo application.</p>
    </div>
  )
}
```

Access at: http://localhost:3000/about

### Task 2: Add a New API Endpoint

**Backend** (`backend/routes/tasks.py`):
```python
@router.get("/api/{user_id}/tasks/stats")
async def get_task_stats(user_id: str, request: Request, db: Session = Depends(get_db)):
    # Verify user_id matches JWT
    if user_id != request.state.user['user_id']:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Query with user isolation
    total = db.query(Task).filter(Task.user_id == user_id).count()
    completed = db.query(Task).filter(Task.user_id == user_id, Task.completed == True).count()

    return {
        "data": {"total": total, "completed": completed},
        "error": None
    }
```

Access at: http://localhost:8000/api/123/tasks/stats

### Task 3: Add Environment Variable

1. Add to `.env`:
   ```bash
   NEW_VARIABLE=some_value
   ```

2. Add to `docker-compose.yml` service:
   ```yaml
   services:
     backend:
       environment:
         - NEW_VARIABLE=${NEW_VARIABLE}
   ```

3. Access in backend:
   ```python
   import os
   value = os.getenv('NEW_VARIABLE')
   ```

4. Restart services:
   ```bash
   docker compose restart
   ```

### Task 4: Install Dependencies

**Frontend**:
```bash
docker compose exec frontend npm install <package>

# Update package.json in Git
git add frontend/package.json frontend/package-lock.json
```

**Backend**:
```bash
docker compose exec backend pip install <package>

# Update requirements.txt
docker compose exec backend pip freeze > backend/requirements.txt

# Commit to Git
git add backend/requirements.txt
```

---

## Troubleshooting

### Problem: Services won't start

**Check Docker**:
```bash
docker ps  # Are containers running?
docker compose logs  # What's the error?
```

**Common causes**:
- Port 3000 or 8000 already in use (stop other services)
- `.env` file missing or incomplete
- Docker not running

### Problem: Frontend can't connect to backend

**Verify**:
1. Backend is running: http://localhost:8000/docs
2. CORS_ORIGINS in `.env` includes `http://localhost:3000`
3. NEXT_PUBLIC_API_URL in `.env` is `http://localhost:8000`

**Check logs**:
```bash
docker compose logs backend | grep CORS
```

### Problem: JWT authentication fails

**Check**:
1. BETTER_AUTH_SECRET is identical in frontend and backend
2. Open `.env` and verify the value
3. Restart services: `docker compose restart`

**Test JWT**:
```bash
# In backend logs, look for JWT verification errors
docker compose logs backend | grep -i jwt
```

### Problem: Database connection fails

**Check**:
1. DATABASE_URL in `.env` is correct
2. Neon PostgreSQL instance is running (check Neon dashboard)
3. Connection string includes `?sslmode=require`

**Test connection**:
```bash
# Check backend startup logs
docker compose logs backend | grep -i database
```

### Problem: Changes not reflecting

**Try**:
```bash
# Hard restart
docker compose down
docker compose up

# Rebuild images
docker compose up --build

# Clear Next.js cache
docker compose exec frontend rm -rf .next
docker compose restart frontend
```

### Problem: Port conflicts

**Error**: "Port 3000 is already allocated"

**Solution**:
```bash
# Find process using port
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Stop the process or change ports in docker-compose.yml
```

---

## Development Tips

### Tip 1: Use API Documentation

Visit http://localhost:8000/docs to:
- See all available endpoints
- Test endpoints interactively
- View request/response schemas
- Generate curl commands

### Tip 2: Follow Spec-Driven Development

Before implementing features:
1. Create specification: `/sp.specify "Feature description"`
2. Generate plan: `/sp.plan`
3. Break down tasks: `/sp.tasks`
4. Implement: `/sp.implement`

See `CLAUDE.md` for complete workflow.

### Tip 3: Read Agent Guidelines

Before coding:
- **Frontend work**: Read `frontend/CLAUDE.md`
- **Backend work**: Read `backend/CLAUDE.md`
- **General guidance**: Read root `CLAUDE.md`

These files contain patterns, anti-patterns, and best practices.

### Tip 4: Check Constitution

Project principles in `.specify/memory/constitution.md`:
- Spec-Driven Development (required)
- Zero Manual Coding (use agents)
- User Data Isolation (security critical)
- JWT-Based Authentication
- RESTful API Conventions
- Responsive Frontend Design
- Minimal Viable Product Focus

### Tip 5: Hot Reload Tips

**Frontend**:
- Changes in `app/`, `components/`, `lib/` reload automatically
- Changes in `package.json` require restart
- Changes in `.env` require restart

**Backend**:
- Changes in `.py` files reload automatically
- Changes in `requirements.txt` require rebuild
- Changes in `.env` require restart

---

## Next Steps

### For New Developers

1. ✅ Complete this quickstart (you're here!)
2. 📋 Read `specs/overview.md` (project goals)
3. 🏗️ Read `specs/architecture.md` (system design)
4. 🔐 Read `specs/001-project-foundation/contracts/jwt-flow.md` (authentication)
5. 📖 Read `README.md` (comprehensive documentation)
6. 💻 Pick a task and start coding!

### For Feature Development

1. **Understand requirements**: Read feature spec in `specs/<feature>/spec.md`
2. **Review plan**: Read `specs/<feature>/plan.md`
3. **Follow tasks**: Implement according to `specs/<feature>/tasks.md`
4. **Test locally**: Verify changes work with Docker Compose
5. **Commit and push**: Follow Git workflow in `CLAUDE.md`

### For Learning More

**Architecture**:
- `specs/001-project-foundation/contracts/architecture-diagram.md` (system overview)
- `specs/001-project-foundation/contracts/jwt-flow.md` (authentication details)
- `specs/001-project-foundation/contracts/directory-structure.md` (file organization)

**Technology Guides**:
- Next.js 16 Docs: https://nextjs.org/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- SQLModel Docs: https://sqlmodel.tiangolo.com
- Better Auth Docs: https://better-auth.com

**Spec-Driven Development**:
- `CLAUDE.md` (workflow phases)
- `.specify/memory/constitution.md` (principles)
- `.specify/templates/` (specification templates)

---

## Quick Reference Card

### Essential URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Web application |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Interactive docs |
| Health Check | http://localhost:8000/health | Backend status |

### Essential Commands

| Task | Command |
|------|---------|
| Start services | `docker compose up` |
| Stop services | `docker compose down` |
| View logs | `docker compose logs -f` |
| Restart service | `docker compose restart <service>` |
| Rebuild images | `docker compose up --build` |
| Access shell | `docker compose exec <service> sh` |

### Essential Files

| File | Purpose |
|------|---------|
| `.env` | Secrets and configuration |
| `docker-compose.yml` | Service orchestration |
| `CLAUDE.md` | Development workflow |
| `specs/overview.md` | Project description |
| `specs/architecture.md` | System design |

### Essential Ports

| Port | Service |
|------|---------|
| 3000 | Frontend (Next.js) |
| 8000 | Backend (FastAPI) |

### Essential Environment Variables

| Variable | Where | Purpose |
|----------|-------|---------|
| BETTER_AUTH_SECRET | Both | JWT signing/verification (MUST MATCH!) |
| DATABASE_URL | Backend | PostgreSQL connection |
| NEXT_PUBLIC_API_URL | Frontend | Backend API URL |
| CORS_ORIGINS | Backend | Allowed frontend origins |

---

## Getting Help

**Documentation**:
1. `README.md` (comprehensive setup)
2. `CLAUDE.md` (development workflow)
3. `specs/` (requirements and architecture)
4. Component `CLAUDE.md` files (frontend/, backend/)

**Troubleshooting**:
1. Check this guide's troubleshooting section
2. Check service logs: `docker compose logs <service>`
3. Review architecture docs for expected behavior
4. Check constitution for project principles

**Resources**:
- Next.js 16: https://nextjs.org/docs
- FastAPI: https://fastapi.tiangolo.com
- SQLModel: https://sqlmodel.tiangolo.com
- Better Auth: https://better-auth.com
- Docker Compose: https://docs.docker.com/compose

---

## Success Checklist

Before starting development, verify:

- ✅ Docker and Docker Compose installed
- ✅ Repository cloned
- ✅ `.env` file created with all variables
- ✅ Neon PostgreSQL database created
- ✅ BETTER_AUTH_SECRET is at least 32 characters
- ✅ Services start with `docker compose up`
- ✅ Frontend loads at http://localhost:3000
- ✅ Backend docs load at http://localhost:8000/docs
- ✅ Read `specs/overview.md` and `specs/architecture.md`
- ✅ Know where to find guidelines (`CLAUDE.md` files)

**You're ready to develop!** 🚀
