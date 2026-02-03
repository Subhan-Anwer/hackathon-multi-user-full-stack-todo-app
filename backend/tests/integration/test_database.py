import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from app.models.models import Task
from app.models.task_crud import create_task, get_tasks_by_user, get_task_by_id, update_task, delete_task
from app.schemas.task_schemas import TaskCreate, TaskUpdate


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


def test_create_task_integration(session: Session):
    """Test creating a task in the database."""
    task_data = TaskCreate(
        title="Integration Test Task",
        description="This is an integration test task"
    )

    created_task = create_task(session, task_data, "user-123")

    assert created_task.id is not None
    assert created_task.title == "Integration Test Task"
    assert created_task.description == "This is an integration test task"
    assert created_task.user_id == "user-123"
    assert created_task.completed is False


def test_get_tasks_by_user_integration(session: Session):
    """Test retrieving all tasks for a specific user."""
    # Create multiple tasks for different users
    task1_data = TaskCreate(title="User 1 Task 1", description="Task for user 1")
    task2_data = TaskCreate(title="User 1 Task 2", description="Another task for user 1")
    task3_data = TaskCreate(title="User 2 Task 1", description="Task for user 2")

    create_task(session, task1_data, "user-1")
    create_task(session, task2_data, "user-1")
    create_task(session, task3_data, "user-2")

    # Get tasks for user-1
    user1_tasks = get_tasks_by_user(session, "user-1")

    assert len(user1_tasks) == 2
    assert all(task.user_id == "user-1" for task in user1_tasks)

    # Get tasks for user-2
    user2_tasks = get_tasks_by_user(session, "user-2")

    assert len(user2_tasks) == 1
    assert user2_tasks[0].user_id == "user-2"


def test_get_task_by_id_integration(session: Session):
    """Test retrieving a specific task by ID for a user."""
    task_data = TaskCreate(title="Specific Task", description="Task to test retrieval")
    created_task = create_task(session, task_data, "user-456")

    # Retrieve the task
    retrieved_task = get_task_by_id(session, created_task.id, "user-456")

    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == "Specific Task"
    assert retrieved_task.user_id == "user-456"

    # Try to retrieve the task with wrong user_id (should return None)
    wrong_user_task = get_task_by_id(session, created_task.id, "wrong-user")
    assert wrong_user_task is None


def test_update_task_integration(session: Session):
    """Test updating a task in the database."""
    # Create a task first
    task_data = TaskCreate(title="Original Task", description="Original description")
    created_task = create_task(session, task_data, "user-update")

    # Update the task
    update_data = TaskUpdate(
        title="Updated Task",
        description="Updated description",
        completed=True
    )

    updated_task = update_task(session, created_task.id, "user-update", update_data)

    assert updated_task is not None
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "Updated description"
    assert updated_task.completed is True


def test_delete_task_integration(session: Session):
    """Test deleting a task from the database."""
    # Create a task first
    task_data = TaskCreate(title="Task to Delete", description="Will be deleted")
    created_task = create_task(session, task_data, "user-delete")

    # Verify task exists
    retrieved_task = get_task_by_id(session, created_task.id, "user-delete")
    assert retrieved_task is not None

    # Delete the task
    delete_success = delete_task(session, created_task.id, "user-delete")
    assert delete_success is True

    # Verify task no longer exists
    deleted_task = get_task_by_id(session, created_task.id, "user-delete")
    assert deleted_task is None


def test_user_data_isolation(session: Session):
    """Test that users can only access their own tasks."""
    # Create tasks for different users
    user1_task_data = TaskCreate(title="User 1 Task", description="Belongs to user 1")
    user2_task_data = TaskCreate(title="User 2 Task", description="Belongs to user 2")

    user1_task = create_task(session, user1_task_data, "user-1")
    user2_task = create_task(session, user2_task_data, "user-2")

    # User 1 should only see their own task
    user1_tasks = get_tasks_by_user(session, "user-1")
    assert len(user1_tasks) == 1
    assert user1_tasks[0].id == user1_task.id

    # User 2 should only see their own task
    user2_tasks = get_tasks_by_user(session, "user-2")
    assert len(user2_tasks) == 1
    assert user2_tasks[0].id == user2_task.id

    # Neither user should see the other's task
    assert user1_task.id not in [task.id for task in user2_tasks]
    assert user2_task.id not in [task.id for task in user1_tasks]


def test_task_validation_on_create(session: Session):
    """Test that validation occurs during task creation via Pydantic schemas."""
    # Test title length validation at the Pydantic schema level
    long_title = "x" * 201  # Exceeds 200 character limit

    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        TaskCreate(title=long_title, description="Too long title")


def test_task_validation_on_update(session: Session):
    """Test that validation occurs during task updates via Pydantic schemas."""
    # Test title length validation at the Pydantic schema level
    long_title = "x" * 201  # Exceeds 200 character limit

    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        TaskUpdate(title=long_title)