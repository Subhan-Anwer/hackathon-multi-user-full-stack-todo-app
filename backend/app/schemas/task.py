from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from pydantic import ConfigDict


class TaskBase(BaseModel):
    """Base task fields shared across schemas."""
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Task title must be 1-255 characters"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Task description, optional, max 1000 characters"
    )

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if v and len(v.strip()) == 0:
            raise ValueError('Title cannot be empty or just whitespace')
        return v.strip() if v else v


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    # Inherit all fields from TaskBase, all required for creation
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)."""
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Task title (1-255 characters) - optional for updates"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Task description, optional, max 1000 characters"
    )
    completed: Optional[bool] = Field(
        None,
        description="Completion status - optional for updates"
    )

    @field_validator('title')
    @classmethod
    def validate_update_title(cls, v):
        if v and len(v.strip()) == 0:
            raise ValueError('Title cannot be empty or just whitespace')
        return v.strip() if v else v


class TaskResponse(TaskBase):
    """Schema for task responses."""
    id: int = Field(..., description="Unique identifier for the task")
    user_id: str = Field(..., description="ID of the user who owns this task")
    completed: bool = Field(default=False, description="Whether the task is completed")
    created_at: datetime = Field(..., description="Timestamp when task was created")
    updated_at: datetime = Field(..., description="Timestamp when task was last updated")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": "user-123",
                "title": "Sample task",
                "description": "This is a sample task description",
                "completed": False,
                "created_at": "2026-02-04T10:00:00Z",
                "updated_at": "2026-02-04T10:00:00Z"
            }
        }
    )