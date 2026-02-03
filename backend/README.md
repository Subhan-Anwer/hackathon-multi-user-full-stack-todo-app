# Backend - FastAPI Todo Application

This is the backend API for the multi-user todo app, built with FastAPI, SQLModel ORM, and PostgreSQL.

## Tech Stack

- **Framework**: FastAPI (Python 3.12+)
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT verification middleware
- **Validation**: Pydantic schemas
- **ASGI Server**: Uvicorn
- **Package Manager**: uv

## Prerequisites

- Python 3.12+
- uv package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Neon PostgreSQL database (sign up at [neon.tech](https://neon.tech))

## Getting Started

### 1. Install Dependencies

Using uv (recommended):

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv pip install --system fastapi uvicorn sqlmodel pyjwt python-dotenv
```

Or using traditional pip (with virtual environment):

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlmodel pyjwt python-dotenv
```

### 2. Configure Environment

Create `.env` file in the `backend/` directory:

```bash
# Copy from example or create manually
cp .env.example .env

# Or create with required variables
cat > .env << 'EOF'
BETTER_AUTH_SECRET=your-secret-key-at-least-32-characters-long
DATABASE_URL=postgresql://username:password@hostname.neon.tech/database?sslmode=require
CORS_ORIGINS=http://localhost:3000
PORT=8000
DEBUG=false
EOF
```

**⚠️ CRITICAL Requirements**:
- `BETTER_AUTH_SECRET` must match the frontend secret exactly
- `DATABASE_URL` must include `?sslmode=require` for Neon
- Get DATABASE_URL from your [Neon Dashboard](https://console.neon.tech)

### 3. Run Development Server

```bash
# Run with hot reload
uvicorn app.main:app --reload

# Or specify custom port
uvicorn app.main:app --reload --port 8080

# Or with host binding for external access
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to see the interactive API documentation (Swagger UI).

## Available Commands

```bash
# Run development server with hot reload
uvicorn app.main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/

# Type checking (if mypy is installed)
mypy app/

# Linting (if ruff is installed)
ruff check app/

# Format code (if black is installed)
black app/

# Sort imports (if isort is installed)
isort app/
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration (environment variables)
│   ├── database.py          # Database connection and session
│   ├── models/              # SQLModel database models
│   │   ├── __init__.py
│   │   ├── task.py          # Task model
│   │   └── user.py          # User model (future)
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   └── task.py          # Task schemas
│   ├── routes/              # API route handlers
│   │   ├── __init__.py
│   │   └── tasks.py         # Task CRUD endpoints
│   ├── middleware/          # Custom middleware
│   │   ├── __init__.py
│   │   └── auth.py          # JWT verification
│   ├── dependencies/        # FastAPI dependencies
│   │   ├── __init__.py
│   │   ├── auth.py          # Auth dependencies
│   │   └── database.py      # Database session
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── jwt.py           # JWT helpers
├── tests/                   # Test files
│   ├── __init__.py
│   ├── test_tasks.py
│   └── conftest.py          # Pytest fixtures
├── .env                     # Environment variables (DO NOT COMMIT)
├── .env.example             # Environment template
├── pyproject.toml           # Python dependencies
├── .python-version          # Python version (3.12)
└── CLAUDE.md                # Development guidelines
```

**⚠️ IMPORTANT**: All application code must be in `app/` directory:
- ✅ Correct: `app/routes/tasks.py`
- ❌ Wrong: `routes/tasks.py`

## Development Guidelines

### User Isolation (Critical)

Every database query MUST filter by authenticated user_id:

```python
# ✅ Good: User-isolated query
tasks = session.exec(
    select(Task).where(Task.user_id == current_user_id)
).all()

# ❌ Bad: No user filtering (security vulnerability!)
tasks = session.exec(select(Task)).all()
```

### JWT Authentication

All protected endpoints verify JWT tokens:

1. Extract token from Authorization header
2. Verify signature using BETTER_AUTH_SECRET
3. Decode token to get user_id
4. Validate URL user_id matches token user_id
5. Filter all queries by user_id

### API Response Format

```python
# Success response
{
    "id": 1,
    "user_id": "user-123",
    "title": "Task title",
    "completed": false,
    "created_at": "2026-02-03T10:30:00Z"
}

# Error response
{
    "detail": "Error message"
}
```

### Type Hints (Required)

Always use type hints:

```python
def get_task_by_id(
    task_id: int,
    user_id: str,
    session: Session
) -> Task | None:
    """Get a task by ID with user isolation."""
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    return session.exec(statement).first()
```

## API Endpoints

All endpoints require JWT authentication:

```
GET     /api/{user_id}/tasks              List all tasks
POST    /api/{user_id}/tasks              Create task
GET     /api/{user_id}/tasks/{id}         Get task details
PUT     /api/{user_id}/tasks/{id}         Update task
DELETE  /api/{user_id}/tasks/{id}         Delete task
PATCH   /api/{user_id}/tasks/{id}/complete Toggle completion
```

## Database Setup

The application uses Neon Serverless PostgreSQL:

1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string (includes `?sslmode=require`)
4. Set as `DATABASE_URL` in `.env`
5. Tables are created automatically on first run (SQLModel.metadata.create_all)

## Common Issues

### Port Already in Use

```bash
# Kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

### Database Connection Failed

- Verify `DATABASE_URL` format includes `?sslmode=require`
- Check Neon database is active in dashboard
- Ensure no IP allowlist restrictions
- Test connection: `psql "<DATABASE_URL>"`

### Import Errors

- Ensure you're in the backend/ directory
- Activate virtual environment if using venv
- Check `PYTHONPATH` if needed: `export PYTHONPATH=$PYTHONPATH:$(pwd)`
- Use correct import: `from app.models.task import Task` (NOT `from models.task`)

### JWT Verification Errors

- Verify `BETTER_AUTH_SECRET` matches frontend exactly
- Check token format: `Authorization: Bearer <token>`
- Ensure no extra spaces in `.env` file

## Testing

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_tasks.py

# Run with coverage report
pytest --cov=app --cov-report=html tests/

# Run and open coverage report
pytest --cov=app --cov-report=html tests/ && open htmlcov/index.html
```

## Security Checklist

Before deploying:

- [ ] User isolation enforced on all endpoints
- [ ] JWT verification on all protected routes
- [ ] No hardcoded secrets (use environment variables)
- [ ] Input validation using Pydantic schemas
- [ ] SQL injection prevented (using SQLModel parameterized queries)
- [ ] CORS configured to allow only known origins
- [ ] HTTPS enforced in production
- [ ] Debug mode disabled in production (`DEBUG=false`)

## Code Quality

- Follow guidelines in `CLAUDE.md`
- Use type hints for all functions
- Write docstrings for public APIs
- Run linter before committing
- Write tests for new endpoints

## Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Neon PostgreSQL](https://neon.tech/docs)

## Additional Documentation

- See `/CLAUDE.md` for project-wide guidelines
- See `CLAUDE.md` (this directory) for backend-specific patterns
- See `/specs/` for feature specifications
- See `/README.md` for complete project setup

---

**Questions?** Check the root `README.md` or `CLAUDE.md` files.
