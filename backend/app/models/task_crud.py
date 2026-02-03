from sqlmodel import Session, select
from typing import Optional
from .models import Task
from ..schemas.task_schemas import TaskCreate, TaskUpdate


def create_task(session: Session, task_data: TaskCreate, user_id: str) -> Task:
    """
    Create a new task for a user with proper user_id association.

    Args:
        session: Database session
        task_data: Task creation data (already validated by Pydantic)
        user_id: ID of the user creating the task

    Returns:
        Created Task instance
    """
    # Create task with validated data (validation handled by Pydantic at API layer)
    task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=user_id,
        completed=False  # Default to False
    )

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task_by_id(session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """
    Get a specific task by ID for the authenticated user.

    Args:
        session: Database session
        task_id: ID of the task to retrieve
        user_id: ID of the user requesting the task

    Returns:
        Task instance if found and belongs to user, None otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    return session.exec(statement).first()


def get_tasks_by_user(session: Session, user_id: str) -> list[Task]:
    """
    Get all tasks for a specific user.

    Args:
        session: Database session
        user_id: ID of the user whose tasks to retrieve

    Returns:
        List of Task instances belonging to the user
    """
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()


def update_task(session: Session, task_id: int, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
    """
    Update a task for the authenticated user.

    Args:
        session: Database session
        task_id: ID of the task to update
        user_id: ID of the user requesting the update
        task_update: Task update data (already validated by Pydantic)

    Returns:
        Updated Task instance if found and belongs to user, None otherwise
    """
    # Get the existing task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        return None

    # Update the task with provided values (validation handled by Pydantic at API layer)
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    # Update the updated_at timestamp
    from datetime import datetime
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int, user_id: str) -> bool:
    """
    Delete a task for the authenticated user.

    Args:
        session: Database session
        task_id: ID of the task to delete
        user_id: ID of the user requesting the deletion

    Returns:
        True if task was deleted, False if task not found or doesn't belong to user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        return False

    session.delete(task)
    session.commit()
    return True


def toggle_task_completion(session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """
    Toggle the completion status of a task for the authenticated user.

    Args:
        session: Database session
        task_id: ID of the task to toggle
        user_id: ID of the user requesting the toggle

    Returns:
        Updated Task instance if found and belongs to user, None otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        return None

    # Toggle completion status
    task.completed = not task.completed

    # Update the updated_at timestamp
    from datetime import datetime
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task