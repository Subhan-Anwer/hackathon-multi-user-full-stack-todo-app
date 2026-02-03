"""Tests for Session Management and Task Route Integration.

This module contains tests for user session validation and task route
integration using dependency override pattern for authentication.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.task_crud import create_task
from app.schemas.task_schemas import TaskCreate


def test_authenticated_user_can_list_own_tasks(client: TestClient, session: Session):
    """Test that authenticated user can list their own tasks."""
    # client fixture authenticates as user-123

    # Create tasks for user-123
    task1 = create_task(session, TaskCreate(title="Task 1"), "user-123")
    task2 = create_task(session, TaskCreate(title="Task 2"), "user-123")

    response = client.get("/api/user-123/tasks")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {t["id"] for t in data} == {task1.id, task2.id}


def test_authenticated_user_can_create_task(client: TestClient):
    """Test that authenticated user can create a task."""
    # client fixture authenticates as user-123

    response = client.post(
        "/api/user-123/tasks",
        json={"title": "New Task", "description": "Description"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Task"
    assert data["user_id"] == "user-123"


def test_authenticated_user_can_update_own_task(client: TestClient, session: Session):
    """Test that authenticated user can update their own task."""
    # Create task for user-123
    task = create_task(session, TaskCreate(title="Original"), "user-123")

    response = client.put(
        f"/api/user-123/tasks/{task.id}",
        json={"title": "Updated Title"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


def test_authenticated_user_can_delete_own_task(client: TestClient, session: Session):
    """Test that authenticated user can delete their own task."""
    # Create task for user-123
    task = create_task(session, TaskCreate(title="To Delete"), "user-123")

    response = client.delete(f"/api/user-123/tasks/{task.id}")

    assert response.status_code == 204

    # Verify deletion
    response = client.get(f"/api/user-123/tasks/{task.id}")
    assert response.status_code == 404


def test_authenticated_user_can_toggle_completion(client: TestClient, session: Session):
    """Test that authenticated user can toggle task completion."""
    # Create task for user-123
    task = create_task(session, TaskCreate(title="Task"), "user-123")

    response = client.patch(f"/api/user-123/tasks/{task.id}/complete")

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True


def test_user_isolation_prevents_cross_user_access(client: TestClient, session: Session):
    """Test that user isolation prevents accessing other users' tasks."""
    # client authenticates as user-123

    # Create task for user-456
    task_456 = create_task(session, TaskCreate(title="User 456 Task"), "user-456")

    # Try to access user-456's tasks
    response = client.get("/api/user-456/tasks")

    # Should return 403 Forbidden
    assert response.status_code == 403


def test_user_cannot_update_other_users_task(client: TestClient, session: Session):
    """Test that user cannot update another user's task."""
    # Create task for user-456
    task_456 = create_task(session, TaskCreate(title="User 456 Task"), "user-456")

    # Try to update as user-123
    response = client.put(
        f"/api/user-456/tasks/{task_456.id}",
        json={"title": "Hacked Title"}
    )

    # Should return 403 Forbidden
    assert response.status_code == 403


def test_user_cannot_delete_other_users_task(client: TestClient, session: Session):
    """Test that user cannot delete another user's task."""
    # Create task for user-456
    task_456 = create_task(session, TaskCreate(title="User 456 Task"), "user-456")

    # Try to delete as user-123
    response = client.delete(f"/api/user-456/tasks/{task_456.id}")

    # Should return 403 Forbidden
    assert response.status_code == 403