# Backend Guidelines - FastAPI Todo App

## ⚠️ CRITICAL: Directory Structure

**ALL APPLICATION CODE MUST BE IN `app/` DIRECTORY**
- ✅ Correct: `backend/app/routes/tasks.py`
- ✅ Correct: `backend/app/models/task.py`
- ❌ Wrong: `backend/routes/tasks.py` (do not create)
- ❌ Wrong: `backend/models/task.py` (do not create)

**Run commands:**
- ✅ Correct: `uvicorn app.main:app --reload`
- ❌ Wrong: `uvicorn main:app --reload`

See `/PROJECT_STRUCTURE.md` for complete details.

## Project Context

This is the backend layer of a multi-user todo application built with FastAPI. It provides RESTful API endpoints, handles JWT authentication from Better Auth, enforces user isolation, and persists data to Neon Serverless PostgreSQL using SQLModel ORM.

## Tech Stack

- **Framework:** FastAPI (Python 3.11+)
- **ORM:** SQLModel (combines SQLAlchemy + Pydantic)
- **Database:** Neon Serverless PostgreSQL
- **Authentication:** JWT verification (tokens issued by Better Auth)
- **Validation:** Pydantic models
- **ASGI Server:** Uvicorn
- **Migration:** Alembic (optional, for production)

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration and environment variables
│   ├── database.py          # Database connection and session management
│   ├── models/              # SQLModel database models
│   │   ├── __init__.py
│   │   ├── task.py          # Task model
│   │   └── user.py          # User model (if needed)
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   └── task.py          # Task schemas
│   ├── routes/              # API route handlers
│   │   ├── __init__.py
│   │   └── tasks.py         # Task CRUD endpoints
│   ├── middleware/          # Custom middleware
│   │   ├── __init__.py
│   │   └── auth.py          # JWT verification middleware
│   ├── dependencies/        # FastAPI dependencies
│   │   ├── __init__.py
│   │   ├── auth.py          # Auth dependencies
│   │   └── database.py      # Database session dependency
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── jwt.py           # JWT utilities
├── tests/                   # Test files
│   ├── __init__.py
│   ├── test_tasks.py
│   └── conftest.py          # Pytest fixtures
├── .env                     # Environment variables (local)
├── .python-version          # Python version for pyenv
├── pyproject.toml           # Poetry dependencies and config
├── README.md
└── CLAUDE.md               # This file
```

## Core Principles

### 1. User Isolation (Critical Security Requirement)

**Every database query MUST filter by the authenticated user's ID:**

```python
# ✅ Good: Filter by user_id
tasks = session.exec(
    select(Task).where(Task.user_id == current_user_id)
).all()

# ❌ Bad: No user filtering - exposes all users' data
tasks = session.exec(select(Task)).all()
```

### 2. JWT Authentication Flow

```
1. Frontend sends request with JWT in Authorization header
2. Middleware extracts and verifies JWT signature
3. Middleware decodes token to get user_id and email
4. Middleware validates user_id matches URL parameter
5. Request proceeds with verified user context
6. Route handler filters data by user_id
```

### 3. API Response Format

**Standard Success Response:**
```python
{
    "id": 1,
    "user_id": "user-uuid",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "created_at": "2026-02-02T10:30:00Z",
    "updated_at": "2026-02-02T10:30:00Z"
}
```

**Standard Error Response:**
```python
{
    "detail": "Error message"
}
```

## Database Models (SQLModel)

### Task Model

```python
# models/task.py
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Task(SQLModel, table=True):
    """Task model with user isolation."""

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False)  # CRITICAL: Always indexed
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user-123",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False
            }
        }
```

**Key Requirements:**
- `user_id` must be **indexed** for query performance
- `user_id` must be **non-nullable** - every task belongs to a user
- All timestamp fields use UTC
- Use `Optional[str]` for nullable string fields

## Pydantic Schemas

### Request/Response Schemas

```python
# schemas/task.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class TaskBase(BaseModel):
    """Base task fields shared across schemas."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass

class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None

class TaskResponse(TaskBase):
    """Schema for task responses."""
    id: int
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

**Important:**
- Use `Field(...)` for required fields
- Use `Field(None, ...)` for optional fields
- Set `model_config = ConfigDict(from_attributes=True)` for ORM compatibility
- Validate string lengths to prevent database errors

## API Routes

### Task CRUD Endpoints

```python
# routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from ..database import get_session
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse
from ..dependencies.auth import get_current_user

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for the authenticated user."""
    # Verify user_id matches authenticated user
    if user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's tasks"
        )

    # Query with user isolation
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the authenticated user."""
    if user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create tasks for another user"
        )

    # Create task with user_id from authenticated user
    task = Task(**task_data.model_dump(), user_id=user_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific task by ID."""
    if user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's tasks"
        )

    # Query with user isolation
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # CRITICAL: User isolation
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a task."""
    if user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update another user's tasks"
        )

    # Fetch task with user isolation
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update only provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a task."""
    if user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete another user's tasks"
        )

    # Fetch task with user isolation
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()
    return None

@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    user_id: str,
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle task completion status."""
    if user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update another user's tasks"
        )

    # Fetch task with user isolation
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle completion
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

## JWT Authentication

### JWT Middleware

```python
# middleware/auth.py
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from ..config import settings

class JWTMiddleware(BaseHTTPMiddleware):
    """Middleware to verify JWT tokens on protected routes."""

    async def dispatch(self, request: Request, call_next):
        # Skip auth for public routes
        if request.url.path in ["/docs", "/redoc", "/openapi.json", "/health"]:
            return await call_next(request)

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header"
            )

        token = auth_header.split(" ")[1]

        try:
            # Verify and decode JWT
            payload = jwt.decode(
                token,
                settings.BETTER_AUTH_SECRET,
                algorithms=["HS256"]
            )

            # Attach user info to request state
            request.state.user = {
                "user_id": payload.get("sub"),  # User ID
                "email": payload.get("email"),
            }

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        response = await call_next(request)
        return response
```

### Auth Dependency

```python
# dependencies/auth.py
from fastapi import Request, HTTPException, status

def get_current_user(request: Request) -> dict:
    """Extract current user from request state."""
    if not hasattr(request.state, "user"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return request.state.user
```

## Database Configuration

### Database Connection

```python
# database.py
from sqlmodel import create_engine, Session, SQLModel
from .config import settings

# Create engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_size=5,
    max_overflow=10,
)

def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session
```

### Configuration

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Database
    DATABASE_URL: str

    # Authentication
    BETTER_AUTH_SECRET: str

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Debug
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### Environment Variables

```bash
# .env
DATABASE_URL=postgresql://user:password@host/database
BETTER_AUTH_SECRET=your-secret-key-min-32-chars-must-match-frontend
DEBUG=false
CORS_ORIGINS=["http://localhost:3000"]
```

**Critical:**
- `BETTER_AUTH_SECRET` must be **identical** in frontend and backend
- Never commit `.env` to version control
- Use strong, random secrets in production

## Main Application

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import create_db_and_tables
from .routes import tasks
from .middleware.auth import JWTMiddleware
from .config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events."""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Todo API",
    description="Multi-user todo API with JWT authentication",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT authentication middleware
app.add_middleware(JWTMiddleware)

# Include routers
app.include_router(tasks.router)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
```

## Error Handling

### Custom Exception Handlers

```python
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )
```

### HTTP Exceptions

```python
from fastapi import HTTPException, status

# 400 Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid input data"
)

# 401 Unauthorized
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Authentication required"
)

# 403 Forbidden
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Cannot access another user's tasks"
)

# 404 Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Task not found"
)

# 422 Unprocessable Entity (automatic from Pydantic validation)
```

## Testing

### Test Configuration

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import get_session

@pytest.fixture(name="session")
def session_fixture():
    """Create in-memory database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with overridden database session."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

### Test Examples

```python
# tests/test_tasks.py
def test_create_task(client: TestClient):
    """Test creating a task."""
    response = client.post(
        "/api/user-123/tasks",
        json={"title": "Test task", "description": "Test description"},
        headers={"Authorization": "Bearer fake-jwt-token"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["user_id"] == "user-123"
    assert data["completed"] is False

def test_get_tasks_user_isolation(client: TestClient):
    """Test that users can only see their own tasks."""
    # Create task for user-123
    client.post(
        "/api/user-123/tasks",
        json={"title": "User 123 task"},
        headers={"Authorization": "Bearer user-123-token"}
    )

    # Try to access as user-456
    response = client.get(
        "/api/user-123/tasks",
        headers={"Authorization": "Bearer user-456-token"}
    )
    assert response.status_code == 403
```

## Code Quality Standards

### Type Hints (Required)

```python
# ✅ Good: Full type hints
def get_task_by_id(task_id: int, user_id: str, session: Session) -> Task | None:
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    return session.exec(statement).first()

# ❌ Bad: No type hints
def get_task_by_id(task_id, user_id, session):
    return session.exec(select(Task).where(...)).first()
```

### Docstrings

```python
def create_task(task_data: TaskCreate, user_id: str, session: Session) -> Task:
    """
    Create a new task for a user.

    Args:
        task_data: Task creation data
        user_id: ID of the user creating the task
        session: Database session

    Returns:
        Created task instance

    Raises:
        HTTPException: If validation fails
    """
    task = Task(**task_data.model_dump(), user_id=user_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Code Formatting

```bash
# Use black for formatting
black app/

# Use isort for import sorting
isort app/

# Use mypy for type checking
mypy app/

# Use ruff for linting
ruff check app/
```

## Security Checklist

- [ ] **User Isolation:** All queries filter by `user_id`
- [ ] **JWT Verification:** All protected routes verify JWT tokens
- [ ] **User ID Validation:** URL `user_id` matches authenticated user
- [ ] **Input Validation:** Use Pydantic schemas for all inputs
- [ ] **SQL Injection:** Use SQLModel parameterized queries (automatic)
- [ ] **Secrets Management:** Never hardcode secrets, use environment variables
- [ ] **CORS Configuration:** Restrict origins to known frontends
- [ ] **Error Messages:** Don't expose sensitive info in error messages
- [ ] **Rate Limiting:** Consider adding rate limiting for production
- [ ] **HTTPS Only:** Enforce HTTPS in production

## Performance Guidelines

### Database Queries

```python
# ✅ Good: Indexed query with specific fields
statement = select(Task.id, Task.title, Task.completed).where(
    Task.user_id == user_id
)

# ❌ Bad: No indexes, fetching unnecessary data
statement = select(Task)  # No user_id filter!
```

### Connection Pooling

```python
# Configure pool size based on expected load
engine = create_engine(
    DATABASE_URL,
    pool_size=10,        # Number of persistent connections
    max_overflow=20,     # Additional connections when pool is full
    pool_timeout=30,     # Seconds to wait for connection
    pool_recycle=3600,   # Recycle connections after 1 hour
)
```

### Pagination (For Large Datasets)

```python
@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Get tasks with pagination."""
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    tasks = session.exec(statement).all()
    return tasks
```

## Development Commands

```bash
# Install dependencies (Poetry)
poetry install

# Activate virtual environment
poetry shell

# Run development server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/

# Type checking
mypy app/

# Linting
ruff check app/

# Format code
black app/ && isort app/

# Database migrations (Alembic)
alembic revision --autogenerate -m "Migration message"
alembic upgrade head
```

## Debugging Tips

### 1. Enable SQL Query Logging
```python
# config.py
DEBUG = True  # Set in .env

# database.py
engine = create_engine(DATABASE_URL, echo=True)  # Logs all SQL queries
```

### 2. Use Debugger
```python
import pdb; pdb.set_trace()  # Python debugger

# Or use debugpy for VS Code
import debugpy
debugpy.listen(5678)
debugpy.wait_for_client()
```

### 3. Log Requests
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Creating task for user {user_id}")
logger.error(f"Failed to create task: {error}")
```

## Common Patterns

### Dependency Injection

```python
# Use FastAPI's dependency injection
from fastapi import Depends

def common_parameters(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}

@router.get("/")
async def get_items(params: dict = Depends(common_parameters)):
    return params
```

### Background Tasks

```python
from fastapi import BackgroundTasks

def send_notification(user_id: str, message: str):
    """Send notification (runs in background)."""
    print(f"Sending to {user_id}: {message}")

@router.post("/")
async def create_task(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks
):
    # Create task
    task = create_task_in_db(task_data)

    # Schedule background task
    background_tasks.add_task(
        send_notification,
        task.user_id,
        f"Task '{task.title}' created"
    )

    return task
```

## Referencing Specs

When implementing features, always reference the relevant specification:
- `@specs/features/task-crud.md` - Task CRUD operations
- `@specs/features/authentication.md` - Authentication requirements
- `@specs/api/rest-endpoints.md` - API endpoint specifications
- `@specs/database/schema.md` - Database schema design

## Key Reminders

1. ✅ **User Isolation** - Every query MUST filter by `user_id`
2. ✅ **JWT Verification** - Verify tokens on all protected routes
3. ✅ **User ID Validation** - URL `user_id` must match authenticated user
4. ✅ **Type Hints** - Use type hints for all function signatures
5. ✅ **Pydantic Validation** - Use schemas for request/response validation
6. ✅ **HTTPException** - Use FastAPI exceptions with proper status codes
7. ✅ **Connection Pooling** - Configure database connection pool
8. ✅ **Error Handling** - Don't expose sensitive info in errors
9. ✅ **UTC Timestamps** - Always use UTC for datetime fields
10. ✅ **Environment Variables** - Never hardcode secrets

## Questions or Issues?

- Check `@specs/` for feature specifications
- Review `/CLAUDE.md` for project-wide guidelines
- Consult FastAPI documentation for framework patterns
- Reference SQLModel documentation for ORM usage
- Review Pydantic documentation for validation patterns
