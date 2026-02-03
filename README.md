# Phase II: Multi-User Todo Application

A production-ready **multi-user todo application** with JWT authentication, persistent storage, and complete user data isolation. Built using **Spec-Driven Development** methodology with Next.js 16+, FastAPI, and Neon PostgreSQL.

## 🎯 Features

This application implements 5 core CRUD operations with secure user authentication:

1. **Add Task** - Create new todo items with title and optional description
2. **Delete Task** - Remove tasks from the list permanently
3. **Update Task** - Modify existing task details (title, description)
4. **View Task List** - Display all user's tasks in an organized list
5. **Mark as Complete** - Toggle task completion status (complete ↔ incomplete)
6. **Authentication** - User signup/signin using Better Auth with JWT tokens

### Key Capabilities

- ✅ **Multi-User Support** - Each user has their own isolated task list
- ✅ **JWT Authentication** - Secure token-based authentication with httpOnly cookies
- ✅ **User Isolation** - Complete separation of user data (zero data leakage)
- ✅ **Persistent Storage** - All data stored in PostgreSQL database
- ✅ **Responsive Design** - Works on mobile, tablet, and desktop
- ✅ **Hot Reload** - Development environment with automatic code refresh

## 🛠️ Tech Stack

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

### Development Tools
- **Methodology**: Spec-Driven Development (Claude Code + Spec-Kit Plus)
- **Containerization**: Docker & Docker Compose
- **Version Control**: Git

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker & Docker Compose** - For running services (recommended)
  - Docker Desktop for Mac/Windows, or Docker Engine + Docker Compose for Linux
  - [Download Docker](https://docs.docker.com/get-docker/)
- **Git** - For cloning the repository
- **Neon PostgreSQL Account** - For database hosting (free tier available)
  - [Sign up at neon.tech](https://neon.tech)

**Optional (for local development without Docker):**
- Node.js 20+ and npm
- Python 3.12+ and uv package manager

## 🚀 Quick Start

Follow these steps to get the application running locally:

### 1. Clone Repository

```bash
git clone <repository-url>
cd hackathon-multi-user-full-stack-todo-app
```

### 2. Configure Environment Variables

```bash
# Copy the environment template
cp .env.example .env

# Edit .env file with your actual values
# Use your favorite text editor (nano, vim, code, etc.)
nano .env
```

**Required values in .env:**
- `BETTER_AUTH_SECRET` - Generate using: `openssl rand -base64 32`
- `DATABASE_URL` - Get from your Neon PostgreSQL dashboard

See the [Environment Variables](#-environment-variables) section below for detailed instructions.

### 3. Get Neon Database Connection String

1. Go to [neon.tech](https://neon.tech) and sign in (or create a free account)
2. Create a new project
3. Copy the connection string from the dashboard
4. Paste it as `DATABASE_URL` in your `.env` file

**Example DATABASE_URL format:**
```
postgresql://username:password@ep-cool-darkness-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### 4. Start Services with Docker Compose

```bash
# Start all services (frontend + backend)
docker-compose up

# Or run in detached mode (background)
docker-compose up -d
```

### 5. Access the Application

Once services are running:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Interactive Swagger UI)

### 6. Create Your Account

1. Navigate to http://localhost:3000
2. Click "Sign Up" to create a new account
3. After signup, you'll be automatically logged in
4. Start creating your tasks!

## 🔐 Environment Variables

### Required Variables

All environment variables must be configured in the `.env` file in the project root. Copy from `.env.example` and fill in the actual values.

#### BETTER_AUTH_SECRET (Critical)

**Purpose**: JWT signing and verification secret

**How to generate**:
```bash
openssl rand -base64 32
```

**⚠️ CRITICAL REQUIREMENT**: This secret MUST be identical in both frontend and backend. The root `.env` file provides this value to both services via Docker Compose.

**Example**:
```bash
BETTER_AUTH_SECRET=your-super-secret-key-at-least-32-characters-long
```

#### DATABASE_URL

**Purpose**: PostgreSQL connection string for backend

**Where to obtain**:
1. Go to your [Neon Dashboard](https://console.neon.tech)
2. Select your project
3. Click "Connection Details"
4. Copy the connection string

**Format**:
```bash
DATABASE_URL=postgresql://username:password@hostname.neon.tech/database?sslmode=require
```

**Important**: Must include `?sslmode=require` for Neon PostgreSQL

#### NEXT_PUBLIC_API_URL

**Purpose**: Backend API base URL for frontend

**Default**: `http://localhost:8000`

**For production**: Change to your deployed backend URL

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### CORS_ORIGINS

**Purpose**: Allowed frontend origins for CORS

**Default**: `http://localhost:3000`

**For production**: Set to your deployed frontend domain

```bash
CORS_ORIGINS=http://localhost:3000
```

#### Optional Variables

```bash
NODE_ENV=development          # development | production | test
PORT=8000                     # Backend server port (default: 8000)
DEBUG=false                   # Enable SQL query logging (true | false)
```

### ⚠️ Security Warning: BETTER_AUTH_SECRET Matching

**The BETTER_AUTH_SECRET must be IDENTICAL in both frontend and backend.**

This is the most common configuration error. If the secrets don't match:
- ❌ Frontend cannot verify backend JWT tokens
- ❌ Backend cannot verify frontend JWT tokens
- ❌ Authentication will fail with "Invalid token" errors

**To verify your configuration**:
```bash
# Check that both services receive the same secret
docker-compose config | grep BETTER_AUTH_SECRET
```

You should see the same value appear twice (once for frontend, once for backend).

## 📁 Project Structure

```
hackathon-multi-user-full-stack-todo-app/
├── frontend/                 # Next.js 16+ application
│   ├── src/
│   │   ├── app/             # App Router pages and layouts
│   │   ├── components/      # React components (ui/ and features/)
│   │   └── lib/             # Utilities (auth, API client)
│   ├── public/              # Static assets
│   ├── Dockerfile           # Frontend container configuration
│   ├── package.json         # Node.js dependencies
│   └── CLAUDE.md            # Frontend development guidelines
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── main.py          # FastAPI app entry point
│   │   ├── routes/          # API route handlers
│   │   ├── middleware/      # Custom middleware (JWT verification)
│   │   ├── models/          # SQLModel database models
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   └── services/        # Business logic services
│   ├── Dockerfile           # Backend container configuration
│   ├── pyproject.toml       # Python dependencies (uv)
│   └── CLAUDE.md            # Backend development guidelines
│
├── specs/                    # Spec-Kit Plus documentation
│   ├── overview.md          # Project overview
│   ├── architecture.md      # System architecture and data flow
│   ├── features/            # Feature specifications
│   ├── api/                 # API endpoint specifications
│   ├── database/            # Database schema specifications
│   └── ui/                  # UI component specifications
│
├── history/                  # Development history
│   ├── prompts/             # Prompt History Records (PHRs)
│   └── adr/                 # Architecture Decision Records
│
├── .specify/                 # Spec-Kit Plus configuration
│   ├── memory/              # Project constitution and memory
│   ├── scripts/             # Automation scripts
│   └── templates/           # Document templates
│
├── docker-compose.yml        # Service orchestration
├── .env                      # Environment variables (DO NOT COMMIT)
├── .env.example              # Environment template
├── .gitignore               # Git ignore rules
├── PROJECT_STRUCTURE.md      # Detailed structure reference
├── CLAUDE.md                 # Root project guidelines
└── README.md                 # This file
```

**Key Directories**:
- `frontend/src/` - All frontend source code (NOT `frontend/app/`)
- `backend/app/` - All backend application code (NOT `backend/routes/`)
- `specs/` - Requirements and architecture documentation
- `history/` - Development decisions and prompt records

See `PROJECT_STRUCTURE.md` for complete directory details.

## 🔄 Development Workflow

This project uses **Spec-Driven Development (SDD)** methodology:

### Phase 1: Specification (`/sp.specify`)
Create feature specification with user scenarios and requirements.

**Output**: `specs/features/<feature>.md`

### Phase 2: Planning (`/sp.plan`)
Generate implementation plan, research decisions, and technical design.

**Output**: `specs/<feature>/plan.md`, `research.md`, `contracts/`

### Phase 3: Task Breakdown (`/sp.tasks`)
Break down plan into actionable, dependency-ordered tasks.

**Output**: `specs/<feature>/tasks.md`

### Phase 4: Implementation (`/sp.implement`)
Execute tasks and build the feature.

**Output**: Working code, tests, documentation

### Phase 5: Documentation
All work is documented via Prompt History Records (PHRs) and Architecture Decision Records (ADRs).

**Output**: `history/prompts/`, `history/adr/`

### Development Guidelines

- All specifications live in `specs/` directory
- Architectural decisions documented in `history/adr/`
- Every implementation references a specification
- Component-specific guidelines in `frontend/CLAUDE.md` and `backend/CLAUDE.md`
- Root guidelines in `CLAUDE.md`

## 🎮 Common Commands

### Using Docker Compose (Recommended)

```bash
# Start all services (frontend + backend)
docker-compose up

# Start in detached mode (background)
docker-compose up -d

# Stop all services
docker-compose down

# View logs from all services
docker-compose logs -f

# View logs from specific service
docker-compose logs -f frontend
docker-compose logs -f backend

# Restart services
docker-compose restart

# Rebuild containers (after dependency changes)
docker-compose up --build

# Access shell in running container
docker-compose exec frontend sh
docker-compose exec backend sh

# Remove all containers and volumes
docker-compose down -v
```

### Frontend (Local Development)

```bash
cd frontend

# Install dependencies
npm install

# Run development server (http://localhost:3000)
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint
```

### Backend (Local Development)

```bash
cd backend

# Install dependencies with uv
uv pip install -e .

# Or install specific packages
uv pip install fastapi uvicorn sqlmodel pyjwt python-dotenv

# Run development server (http://localhost:8000)
uvicorn app.main:app --reload

# Run with custom port
uvicorn app.main:app --reload --port 8080

# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

## 🔧 Troubleshooting

### Port Already in Use

**Problem**: Error message "port is already allocated" or "address already in use"

**Solution**:
```bash
# Find process using port 3000 (frontend)
lsof -i :3000
kill -9 <PID>

# Find process using port 8000 (backend)
lsof -i :8000
kill -9 <PID>

# Or change ports in .env file
PORT=8001  # Backend port
```

### Environment Variable Errors

**Problem**: "Missing environment variable" or "Could not load .env file"

**Solution**:
1. Verify `.env` file exists in project root
   ```bash
   ls -la .env
   ```

2. Check `.env` has all required variables:
   ```bash
   cat .env
   ```

3. Ensure no extra spaces around `=` signs:
   ```bash
   # ✅ Correct
   BETTER_AUTH_SECRET=abc123

   # ❌ Wrong (spaces around =)
   BETTER_AUTH_SECRET = abc123
   ```

4. Restart Docker Compose to reload environment:
   ```bash
   docker-compose down
   docker-compose up
   ```

### BETTER_AUTH_SECRET Mismatch

**Problem**: "Invalid token" or "Unauthorized" errors despite logging in

**Solution**:
1. Verify both services use the same secret:
   ```bash
   docker-compose config | grep BETTER_AUTH_SECRET
   ```

2. Check `.env` file has only ONE `BETTER_AUTH_SECRET` entry:
   ```bash
   grep BETTER_AUTH_SECRET .env
   ```

3. Generate a new secret and update `.env`:
   ```bash
   openssl rand -base64 32
   ```

4. Restart all services:
   ```bash
   docker-compose down
   docker-compose up
   ```

### Database Connection Issues

**Problem**: "Could not connect to database" or "Connection refused"

**Solution**:
1. Verify `DATABASE_URL` format includes `?sslmode=require`:
   ```bash
   echo $DATABASE_URL
   # Should end with: ?sslmode=require
   ```

2. Check Neon database is active in [Neon Dashboard](https://console.neon.tech)

3. Verify network connectivity:
   ```bash
   ping <your-neon-hostname>.neon.tech
   ```

4. Test connection with psql (if installed):
   ```bash
   psql "<your-DATABASE_URL>"
   ```

5. Check for IP allowlist restrictions in Neon dashboard

### Docker Not Installed

**Problem**: "docker: command not found" or "docker-compose: command not found"

**Solution**:
1. Install Docker Desktop:
   - **Mac**: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
   - **Windows**: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
   - **Linux**: [Docker Engine](https://docs.docker.com/engine/install/)

2. Verify installation:
   ```bash
   docker --version
   docker-compose --version
   ```

3. Ensure Docker daemon is running:
   ```bash
   docker ps
   ```

### Hot Reload Not Working

**Problem**: Code changes don't trigger automatic refresh

**Solution**:

**Frontend**:
1. Verify volume mount in docker-compose.yml:
   ```yaml
   volumes:
     - ./frontend:/app
     - /app/node_modules
   ```

2. Check Next.js dev server is running:
   ```bash
   docker-compose logs frontend | grep "ready"
   ```

**Backend**:
1. Verify volume mount in docker-compose.yml:
   ```yaml
   volumes:
     - ./backend:/app
   ```

2. Check uvicorn reload is enabled:
   ```bash
   docker-compose logs backend | grep "reload"
   ```

3. Restart services:
   ```bash
   docker-compose restart
   ```

## 🏗️ Architecture

### High-Level Overview

```
User Browser
    ↓
Next.js Frontend (Port 3000)
    ↓ HTTP + JWT (Authorization: Bearer <token>)
FastAPI Backend (Port 8000)
    ↓ SQL Queries (user-filtered)
Neon PostgreSQL
```

### Authentication Flow

1. User logs in → Better Auth creates JWT token
2. Token stored in httpOnly cookie (JavaScript cannot access)
3. Browser automatically includes cookie in requests
4. Backend verifies JWT signature and extracts user_id
5. All database queries filtered by user_id

### User Data Isolation

Every user sees only their own data. Enforced at multiple levels:

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

For detailed architecture documentation, see `specs/architecture.md`.

## 🤝 Contributing

This project is built using Spec-Driven Development methodology. If you want to contribute:

### Git Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following project guidelines

3. **Commit with clear messages**:
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

4. **Push to remote**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** on GitHub

### Branch Naming Conventions

- `feature/` - New features (e.g., `feature/task-filtering`)
- `fix/` - Bug fixes (e.g., `fix/auth-token-expiry`)
- `docs/` - Documentation updates (e.g., `docs/update-readme`)
- `refactor/` - Code refactoring (e.g., `refactor/api-client`)

### Commit Message Conventions

Use conventional commit format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, no logic change)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

**Examples**:
```
feat(tasks): add task filtering by status
fix(auth): resolve token expiration issue
docs(readme): update troubleshooting section
```

### Prompt History Records (PHRs)

When using Claude Code for development:

1. Every implementation session generates a PHR automatically
2. PHRs are stored in `history/prompts/<feature>/`
3. Never manually create or edit PHRs
4. PHRs track the development process for learning and traceability

### Code Quality Standards

- **Frontend**: Follow `frontend/CLAUDE.md` guidelines
- **Backend**: Follow `backend/CLAUDE.md` guidelines
- **Root**: Follow `CLAUDE.md` project-wide policies
- **Type Safety**: Use TypeScript (frontend) and type hints (backend)
- **Testing**: Write tests for new features
- **Security**: Never hardcode secrets, always enforce user isolation

## 📚 Additional Documentation

- **[Project Structure](PROJECT_STRUCTURE.md)** - Detailed directory organization
- **[Architecture](specs/architecture.md)** - System design and data flow
- **[API Endpoints](specs/api/)** - API endpoint specifications
- **[Database Schema](specs/database/)** - Data models and relationships
- **[Frontend Guidelines](frontend/CLAUDE.md)** - Next.js 16 patterns
- **[Backend Guidelines](backend/CLAUDE.md)** - FastAPI patterns
- **[Constitution](.specify/memory/constitution.md)** - Project principles

## 📝 License

This is a hackathon project for educational purposes.

---

**Questions or Issues?**

1. Check `/specs/` for requirements and architecture
2. Review `PROJECT_STRUCTURE.md` for directory organization
3. Consult component `CLAUDE.md` files for implementation guidance
4. Reference `.specify/memory/constitution.md` for project principles

**Built with Spec-Driven Development using Claude Code** 🤖
