from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..db.db import get_session_dependency
from ..models.models import Task
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse
from ..models.task_crud import (
    create_task,
    get_task_by_id,
    get_tasks_by_user,
    update_task,
    delete_task,
    toggle_task_completion
)
from ..dependencies.auth import get_current_user_id, verify_user_id_match
import logging

# Set up logging for this module
logger = logging.getLogger(__name__)

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
    try:
        # Verify user_id in URL matches authenticated user
        verify_user_id_match(user_id, token_user_id)

        logger.info(f"Fetching tasks for user: {user_id}")
        tasks = get_tasks_by_user(session=session, user_id=user_id)
        logger.info(f"Successfully retrieved {len(tasks)} tasks for user: {user_id}")
        return tasks

    except HTTPException:
        # Re-raise HTTP exceptions (like 403 Forbidden)
        logger.warning(f"Authorization failed for user {user_id}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching tasks for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving tasks"
        )


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
    try:
        # Verify user_id in URL matches authenticated user
        verify_user_id_match(user_id, token_user_id)

        logger.info(f"Creating new task for user: {user_id}")
        task = create_task(session=session, task_data=task_data, user_id=user_id)
        logger.info(f"Successfully created task with ID: {task.id} for user: {user_id}")
        return task

    except ValueError as e:
        logger.warning(f"Validation error creating task for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like 403 Forbidden)
        logger.warning(f"Authorization failed for user {user_id}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating task for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while creating task"
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
    try:
        # Verify user_id in URL matches authenticated user
        verify_user_id_match(user_id, token_user_id)

        logger.info(f"Fetching task {task_id} for user: {user_id}")
        task = get_task_by_id(session=session, task_id=task_id, user_id=user_id)
        if not task:
            logger.info(f"Task {task_id} not found for user: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )

        logger.info(f"Successfully retrieved task {task_id} for user: {user_id}")
        return task

    except HTTPException:
        # Re-raise HTTP exceptions (like 403 Forbidden, 404 Not Found)
        logger.warning(f"Error accessing task {task_id} for user {user_id}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving task"
        )


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
    try:
        # Verify user_id in URL matches authenticated user
        verify_user_id_match(user_id, token_user_id)

        logger.info(f"Updating task {task_id} for user: {user_id}")

        # Validate updated data first
        if task_data.title is not None and len(task_data.title) > 255:
            logger.warning(f"Title validation failed for task {task_id}, user {user_id}: too long")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Title must be 255 characters or less"
            )
        if task_data.description is not None and len(task_data.description) > 1000:
            logger.warning(f"Description validation failed for task {task_id}, user {user_id}: too long")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Description must be 1000 characters or less"
            )

        updated_task = update_task(
            session=session,
            task_id=task_id,
            user_id=user_id,
            task_update=task_data
        )

        if not updated_task:
            logger.info(f"Task {task_id} not found for user: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )

        logger.info(f"Successfully updated task {task_id} for user: {user_id}")
        return updated_task

    except HTTPException:
        # Re-raise HTTP exceptions (like 403 Forbidden, 404 Not Found, 422 Validation errors)
        logger.warning(f"Error updating task {task_id} for user {user_id}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while updating task"
        )


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
    try:
        # Verify user_id in URL matches authenticated user
        verify_user_id_match(user_id, token_user_id)

        logger.info(f"Deleting task {task_id} for user: {user_id}")
        success = delete_task(session=session, task_id=task_id, user_id=user_id)
        if not success:
            logger.info(f"Task {task_id} not found for user: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )

        logger.info(f"Successfully deleted task {task_id} for user: {user_id}")
        return None  # 204 No Content

    except HTTPException:
        # Re-raise HTTP exceptions (like 403 Forbidden, 404 Not Found)
        logger.warning(f"Error deleting task {task_id} for user {user_id}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while deleting task"
        )


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
    try:
        # Verify user_id in URL matches authenticated user
        verify_user_id_match(user_id, token_user_id)

        logger.info(f"Toggling completion status for task {task_id} for user: {user_id}")
        updated_task = toggle_task_completion(session=session, task_id=task_id, user_id=user_id)
        if not updated_task:
            logger.info(f"Task {task_id} not found for user: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to user"
            )

        logger.info(f"Successfully toggled completion status for task {task_id} (now {updated_task.completed}) for user: {user_id}")
        return updated_task

    except HTTPException:
        # Re-raise HTTP exceptions (like 403 Forbidden, 404 Not Found)
        logger.warning(f"Error toggling completion status for task {task_id} for user {user_id}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error toggling completion status for task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while toggling task completion"
        )


