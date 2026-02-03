from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..db.db import get_session_dependency
from ..models.models import Task
from ..schemas.task_schemas import TaskCreate, TaskUpdate, TaskResponse
from ..models.task_crud import (
    create_task,
    get_task_by_id,
    get_tasks_by_user,
    update_task,
    delete_task,
    toggle_task_completion
)
from ..dependencies.auth import get_current_user_id, verify_user_id_match

# Create router with prefix for user-scoped tasks
router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    user_id: str,
    token_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session_dependency)
):
    """
    Get all tasks for the authenticated user.

    Args:
        user_id: ID of the user whose tasks to retrieve
        token_user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        List of tasks belonging to the user
    """
    # Verify user_id in URL matches authenticated user
    verify_user_id_match(user_id, token_user_id)

    tasks = get_tasks_by_user(session=session, user_id=user_id)
    return tasks


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    user_id: str,
    task_data: TaskCreate,
    token_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session_dependency)
):
    """
    Create a new task for the authenticated user.

    Args:
        user_id: ID of the user creating the task
        task_data: Task creation data
        token_user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        Created task
    """
    # Verify user_id in URL matches authenticated user
    verify_user_id_match(user_id, token_user_id)

    try:
        task = create_task(session=session, task_data=task_data, user_id=user_id)
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_specific_task(
    user_id: str,
    task_id: int,
    token_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session_dependency)
):
    """
    Get a specific task by ID for the authenticated user.

    Args:
        user_id: ID of the user requesting the task
        task_id: ID of the task to retrieve
        token_user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        Task if found and belongs to user
    """
    # Verify user_id in URL matches authenticated user
    verify_user_id_match(user_id, token_user_id)

    task = get_task_by_id(session=session, task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_existing_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    token_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session_dependency)
):
    """
    Update a task for the authenticated user.

    Args:
        user_id: ID of the user requesting the update
        task_id: ID of the task to update
        task_data: Task update data
        token_user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        Updated task
    """
    # Verify user_id in URL matches authenticated user
    verify_user_id_match(user_id, token_user_id)

    updated_task = update_task(
        session=session,
        task_id=task_id,
        user_id=user_id,
        task_update=task_data
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    # Validate updated data
    try:
        if task_data.title and len(task_data.title) > 200:
            raise ValueError("Title must be 200 characters or less")
        if task_data.description and len(task_data.description) > 1000:
            raise ValueError("Description must be 1000 characters or less")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_task(
    user_id: str,
    task_id: int,
    token_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session_dependency)
):
    """
    Delete a task for the authenticated user.

    Args:
        user_id: ID of the user requesting the deletion
        task_id: ID of the task to delete
        token_user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        204 No Content on successful deletion
    """
    # Verify user_id in URL matches authenticated user
    verify_user_id_match(user_id, token_user_id)

    success = delete_task(session=session, task_id=task_id, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return None  # 204 No Content


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion_status(
    user_id: str,
    task_id: int,
    token_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session_dependency)
):
    """
    Toggle the completion status of a task for the authenticated user.

    Args:
        user_id: ID of the user requesting the toggle
        task_id: ID of the task to toggle
        token_user_id: User ID extracted from JWT token
        session: Database session

    Returns:
        Updated task with toggled completion status
    """
    # Verify user_id in URL matches authenticated user
    verify_user_id_match(user_id, token_user_id)

    updated_task = toggle_task_completion(session=session, task_id=task_id, user_id=user_id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to user"
        )

    return updated_task


