"""Test suite for authentication flow with user isolation using dependency override."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.task_crud import create_task
from app.schemas.task_schemas import TaskCreate


def test_valid_authentication_flow(client: TestClient, session: Session):
    """Test that authenticated user can access their own tasks."""
    # client fixture already authenticates as user-123

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


def test_correct_user_id_validation(client: TestClient, session: Session):
    """Test that URL user_id must match authenticated user."""
    # client fixture authenticates as user-123

    # Try to access user-456's tasks using user-123's authentication
    response = client.get("/api/user-456/tasks")

    # Should return 403 Forbidden because URL user_id doesn't match authenticated user_id
    assert response.status_code == 403


def test_public_endpoints_accessible(client: TestClient):
    """Test that public endpoints don't require authentication."""
    response = client.get("/health")

    # Health check should be accessible
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_task_with_valid_auth(client: TestClient):
    """Test creating a task with valid authentication."""
    # client fixture authenticates as user-123

    # Create a task
    response = client.post(
        "/api/user-123/tasks",
        json={"title": "New Task", "description": "Task Description"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Task"
    assert data["user_id"] == "user-123"
    assert data["completed"] is False


def test_create_task_with_mismatched_user_id(client: TestClient):
    """Test creating a task with mismatched user_id."""
    # client fixture authenticates as user-123

    # Try to create a task for user-456 using user-123's authentication
    response = client.post(
        "/api/user-456/tasks",
        json={"title": "New Task", "description": "Task Description"}
    )

    # Should return 403 Forbidden
    assert response.status_code == 403