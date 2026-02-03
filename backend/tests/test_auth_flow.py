"""Test suite for authentication flow with JWT verification and user isolation."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from unittest.mock import patch
import jwt
from datetime import datetime, timedelta

from app.main import app
from app.db.db import get_session_dependency
from app.models.models import Task


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
        yield session

    app.dependency_overrides[get_session_dependency] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def create_mock_jwt_token(user_id: str, email: str = "test@example.com", secret: str = "test_secret"):
    """Create a mock JWT token for testing."""
    payload = {
        "sub": user_id,  # User ID
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "iss": "better-auth"
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


def test_valid_authentication_flow(client: TestClient, session: Session):
    """Test that valid JWT tokens allow access to user's own tasks."""
    # Create a mock JWT token for user-123
    token = create_mock_jwt_token("user-123")

    # Create a task for user-123
    from app.models.task_crud import create_task
    from app.schemas.task_schemas import TaskCreate

    task_data = TaskCreate(title="Test Task", description="Test Description")
    created_task = create_task(session=session, task_data=task_data, user_id="user-123")

    # Test getting tasks for user-123 with valid token
    response = client.get(
        f"/api/user-123/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == created_task.id
    assert data[0]["user_id"] == "user-123"


def test_cross_user_access_denied(client: TestClient, session: Session):
    """Test that users cannot access other users' tasks."""
    # Create a mock JWT token for user-123
    token_user_123 = create_mock_jwt_token("user-123")

    # Create a task for user-456
    from app.models.task_crud import create_task
    from app.schemas.task_schemas import TaskCreate

    task_data = TaskCreate(title="User 456 Task", description="User 456 Description")
    created_task = create_task(session=session, task_data=task_data, user_id="user-456")

    # Try to access user-456's tasks using user-123's token
    response = client.get(
        f"/api/user-456/tasks",
        headers={"Authorization": f"Bearer {token_user_123}"}
    )

    # Should return 403 Forbidden due to user isolation
    assert response.status_code == 403


def test_invalid_token_rejected(client: TestClient):
    """Test that invalid JWT tokens are rejected."""
    # Use an invalid token
    invalid_token = "invalid.token.here"

    response = client.get(
        f"/api/user-123/tasks",
        headers={"Authorization": f"Bearer {invalid_token}"}
    )

    # Should return 401 Unauthorized
    assert response.status_code == 401


def test_expired_token_rejected(client: TestClient):
    """Test that expired JWT tokens are rejected."""
    # Create an expired token
    expired_payload = {
        "sub": "user-123",
        "email": "test@example.com",
        "exp": datetime.utcnow() - timedelta(hours=1),  # Expired 1 hour ago
        "iat": datetime.utcnow() - timedelta(hours=2),
        "iss": "better-auth"
    }
    expired_token = jwt.encode(expired_payload, "test_secret", algorithm="HS256")

    response = client.get(
        f"/api/user-123/tasks",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    # Should return 401 Unauthorized
    assert response.status_code == 401


def test_missing_authorization_header(client: TestClient):
    """Test that requests without authorization header are rejected."""
    response = client.get("/api/user-123/tasks")

    # Should return 401 Unauthorized
    assert response.status_code == 401


def test_invalid_authorization_format(client: TestClient):
    """Test that malformed authorization headers are rejected."""
    response = client.get(
        "/api/user-123/tasks",
        headers={"Authorization": "InvalidFormat"}
    )

    # Should return 401 Unauthorized
    assert response.status_code == 401


def test_correct_user_id_validation(client: TestClient, session: Session):
    """Test that URL user_id matches JWT token user_id."""
    # Create a mock JWT token for user-123
    token_user_123 = create_mock_jwt_token("user-123")

    # Try to access user-456's tasks using user-123's token in URL
    response = client.get(
        f"/api/user-456/tasks",
        headers={"Authorization": f"Bearer {token_user_123}"}
    )

    # Should return 403 Forbidden because URL user_id doesn't match token user_id
    assert response.status_code == 403


def test_public_endpoints_accessible(client: TestClient):
    """Test that public endpoints don't require authentication."""
    response = client.get("/health")

    # Health check should be accessible without auth
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_task_with_valid_auth(client: TestClient):
    """Test creating a task with valid authentication."""
    # Create a mock JWT token for user-123
    token = create_mock_jwt_token("user-123")

    # Create a task
    response = client.post(
        "/api/user-123/tasks",
        json={"title": "New Task", "description": "Task Description"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Task"
    assert data["user_id"] == "user-123"
    assert data["completed"] is False


def test_create_task_with_mismatched_user_id(client: TestClient):
    """Test creating a task with mismatched user_id."""
    # Create a mock JWT token for user-123
    token_user_123 = create_mock_jwt_token("user-123")

    # Try to create a task for user-456 using user-123's token
    response = client.post(
        "/api/user-456/tasks",
        json={"title": "New Task", "description": "Task Description"},
        headers={"Authorization": f"Bearer {token_user_123}"}
    )

    # Should return 403 Forbidden
    assert response.status_code == 403