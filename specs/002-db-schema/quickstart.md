# Quickstart: Database Schema & SQLModel Implementation

## Prerequisites

- Python 3.11+
- uv package manager for dependency management
- PostgreSQL database (Neon serverless recommended)
- Environment variables configured:
  - `DATABASE_URL`: PostgreSQL connection string

## Virtual Environment and Dependency Management

1. **Setup uv package manager** (if not already installed):
   ```bash
   pip install uv
   # Or install via other methods as per uv documentation
   ```

2. **Navigate to backend directory and setup virtual environment**:
   ```bash
   cd backend
   uv venv  # Creates virtual environment in .venv directory
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies using uv**:
   ```bash
   # Activate virtual environment first (as shown above)
   uv pip install sqlmodel pydantic psycopg2-binary fastapi uvicorn python-multipart python-jose[cryptography] passlib[bcrypt] python-dotenv
   ```

4. **Alternative: Using pyproject.toml approach** (recommended):
   ```bash
   # If pyproject.toml exists in backend/
   cd backend
   uv venv
   source .venv/bin/activate
   uv pip install -e .  # Installs project dependencies from pyproject.toml
   ```

5. **Dependency Management Commands**:
   ```bash
   # Add new dependency
   uv pip install <package-name>

   # Export dependencies (if using requirements.txt approach)
   uv pip freeze > requirements.txt

   # Install from requirements.txt
   uv pip install -r requirements.txt
   ```

## Setup Database Models

1. **With virtual environment activated**, create SQLModel Task Model:
   - Location: `backend/app/models/models.py`
   - Implements the Task entity with all 7 required fields
   - Includes proper constraints and validation

2. **Configure Database Connection**:
   - Location: `backend/app/db/db.py`
   - Creates SQLModel engine from DATABASE_URL
   - Sets up session factory for dependency injection

## Key Implementation Steps

1. **Define Task Model**:
   ```python
   from sqlmodel import SQLModel, Field, create_engine, Session
   from typing import Optional
   from datetime import datetime
   import uuid

   class Task(SQLModel, table=True):
       id: Optional[int] = Field(default=None, primary_key=True)
       user_id: str = Field(foreign_key="users.id", nullable=False)
       title: str = Field(max_length=200, nullable=False)
       description: Optional[str] = Field(max_length=1000, default=None)
       completed: bool = Field(default=False, nullable=False)
       created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
       updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
   ```

2. **Set Up Database Connection**:
   - Initialize SQLModel engine with connection pooling
   - Configure session dependency for FastAPI
   - Create tables using `SQLModel.metadata.create_all(engine)`

3. **Implement Query Functions**:
   - Create, read, update, delete operations
   - All operations must filter by user_id for isolation
   - Proper error handling and validation

## Environment Configuration

Create `.env` file with:
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-jwt-secret-key
```

## Testing the Implementation

1. **Unit Tests**: Verify model constraints and validation
   ```bash
   # Ensure virtual environment is activated
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install pytest pytest-asyncio
   pytest tests/unit/test_models.py -v
   ```

2. **Integration Tests**: Test database operations with real PostgreSQL
   ```bash
   # Run integration tests with activated virtual environment
   source .venv/bin/activate
   pytest tests/integration/test_database.py -v
   ```

3. **Isolation Tests**: Confirm user data isolation works correctly
   ```bash
   # Run all tests with coverage
   source .venv/bin/activate
   pytest tests/ --cov=backend.app --cov-report=html
   ```

## Running the Application

1. **Start the backend server**:
   ```bash
   # Activate virtual environment
   source .venv/bin/activate
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Using the virtual environment for development**:
   ```bash
   # Always activate the virtual environment before development
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   # Install additional development dependencies
   uv pip install black isort flake8 mypy
   ```

## Next Steps

After implementing the models:
1. Create API endpoints that use the Task model
2. Implement user authentication and JWT verification
3. Add proper error handling and validation
4. Set up automated testing pipeline