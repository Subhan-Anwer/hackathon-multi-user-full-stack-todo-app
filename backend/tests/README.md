# Backend Tests Documentation

This document explains the testing approach and patterns used in the backend test suite.

## Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── test_auth_flow.py        # Authentication flow tests
├── test_session_management.py # Session management tests
├── integration/             # Integration tests
│   └── test_database.py     # Database integration tests
└── unit/                   # Unit tests
    └── test_models.py       # Model unit tests
```

## Authentication Testing Pattern

The authentication tests use a dependency override pattern to mock JWT authentication without requiring real tokens:

### Core Fixtures

#### `client` Fixture
- Authenticates as user-123 by default
- Uses dependency override to mock `get_current_user_id`
- Provides database session isolation

#### `client_user_456` Fixture
- Authenticates as user-456 for cross-user testing
- Uses dependency override to mock `get_current_user_id`
- Enables testing of user isolation

### Example Usage

```python
def test_valid_authentication_flow(client: TestClient, session: Session):
    """Test that authenticated user can access their own tasks."""
    # client fixture authenticates as user-123

    # Create a task for user-123
    task_data = TaskCreate(title="Test Task", description="Test Description")
    created_task = create_task(session=session, task_data=task_data, user_id="user-123")

    # Test getting tasks for user-123
    response = client.get("/api/user-123/tasks")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == created_task.id
    assert data[0]["user_id"] == "user-123"
```

## Dependency Override Pattern

The test suite uses FastAPI's dependency override system to bypass JWT verification:

```python
# In conftest.py
@pytest.fixture(name="client")
def client_fixture(session: Session, mock_user_id: str):
    """Create test client with mocked auth and database."""
    def get_session_override():
        return session

    def get_current_user_id_override(authorization: str = "Bearer test-token"):
        # Mock function that accepts the header parameter but returns a hardcoded user ID
        return mock_user_id

    app.dependency_overrides[get_session_dependency] = get_session_override
    app.dependency_overrides[get_current_user_id] = get_current_user_id_override

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()
```

This approach:
- Eliminates need for real JWT tokens in tests
- Provides deterministic user authentication
- Enables cross-user access testing
- Improves test performance and reliability

## Cross-User Access Testing

Tests verify user isolation by creating multiple authenticated clients:

```python
def test_cross_user_access_denied(client: TestClient, client_user_456, session: Session):
    """Test that users cannot access other users' tasks."""
    # client fixture authenticates as user-123
    # client_user_456 fixture authenticates as user-456

    # Create a task for user-456
    task_data = TaskCreate(title="User 456 Task", description="User 456 Description")
    created_task = create_task(session=session, task_data=task_data, user_id="user-456")

    # Try to access user-456's tasks using user-123's authentication
    response = client.get("/api/user-456/tasks")

    # Should return 403 Forbidden due to user isolation
    assert response.status_code == 403
```

## Test Retry Configuration

Flaky tests are handled with pytest-rerunfailures:

```ini
# In pyproject.toml
[tool.pytest.ini_options]
addopts = "--reruns 3 --reruns-delay 1"
```

This automatically retries failed tests up to 3 times with 1 second delay between attempts.

## Running Tests

### All Tests
```bash
pytest
```

### Specific Test File
```bash
pytest tests/test_auth_flow.py
```

### With Verbose Output
```bash
pytest -v
```

### With Coverage
```bash
pytest --cov=app
```

## Test Categories

### Authentication Flow Tests (`test_auth_flow.py`)
- User authentication and authorization
- Cross-user access prevention
- Public endpoint accessibility
- Task creation/deletion with auth

### Session Management Tests (`test_session_management.py`)
- User session validation
- Task CRUD operations for authenticated users
- User isolation verification
- Session expiry handling

### Database Integration Tests (`integration/test_database.py`)
- Database model validation
- CRUD operations at the database level
- Data integrity checks
- Relationship validation

### Unit Tests (`unit/test_models.py`)
- Individual model validation
- Field constraints verification
- Default value validation

## Best Practices

### 1. Use Descriptive Test Names
```python
def test_authenticated_user_can_create_task():  # Good
def test_task_creation():  # Less descriptive
```

### 2. Include Docstrings
```python
def test_user_isolation_prevents_cross_user_access():
    """Test that user isolation prevents accessing other users' tasks."""
    # Test implementation
```

### 3. Test Both Positive and Negative Cases
```python
def test_valid_authentication_flow():  # Positive case
def test_cross_user_access_denied():  # Negative case (security)
```

### 4. Use Type Hints for Fixtures
```python
def test_authenticated_user_can_create_task(
    client: TestClient,
    session: Session
):
```

## Troubleshooting

### Tests Failing Due to Authentication
- Verify dependency overrides are properly configured
- Check that fixture isolation is working
- Ensure `app.dependency_overrides.clear()` is called

### Database Isolation Issues
- Verify each test uses its own session fixture
- Check that database operations are properly isolated
- Ensure transactions are properly rolled back

### Cross-User Access Not Blocked
- Verify `verify_user_id_match` function is working
- Check that URL user_id matches authenticated user_id
- Validate that dependency overrides return correct user IDs

## Maintenance

When adding new authentication functionality:
1. Add corresponding test cases
2. Verify user isolation is maintained
3. Test both positive and negative scenarios
4. Ensure dependency overrides work correctly