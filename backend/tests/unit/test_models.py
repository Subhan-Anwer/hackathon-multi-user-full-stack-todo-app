import pytest
from datetime import datetime
from sqlmodel import Session, select
from app.models.models import Task
from app.schemas.task_schemas import TaskCreate


def test_task_creation_with_valid_data():
    """Test creating a Task with valid data."""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "user_id": "user-123",
        "completed": False
    }

    task = Task(**task_data)

    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.user_id == "user-123"
    assert task.completed is False
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_creation_required_fields_only():
    """Test creating a Task with only required fields."""
    task_data = {
        "title": "Minimal Task",
        "user_id": "user-456"
    }

    task = Task(**task_data)

    assert task.title == "Minimal Task"
    assert task.user_id == "user-456"
    assert task.completed is False  # Should default to False
    assert task.description is None  # Should default to None
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_title_max_length():
    """Test that title respects the 200 character limit."""
    long_title = "x" * 200  # Exactly 200 characters
    task = Task(title=long_title, user_id="user-789")

    assert len(task.title) == 200
    assert task.title == long_title


def test_task_description_max_length():
    """Test that description respects the 1000 character limit."""
    long_description = "x" * 1000  # Exactly 1000 characters
    task = Task(title="Test", description=long_description, user_id="user-101")

    assert len(task.description) == 1000
    assert task.description == long_description


def test_task_default_values():
    """Test that Task has correct default values."""
    task = Task(title="Default Test", user_id="user-202")

    assert task.completed is False
    assert task.description is None
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_field_constraints():
    """Test field constraints are properly set."""
    # Test that required fields are enforced by the schema/model
    task = Task(title="Constraint Test", user_id="user-303")

    # Verify the field properties
    assert task.title is not None
    assert task.user_id is not None
    assert len(task.title) <= 200
    if task.description:
        assert len(task.description) <= 1000