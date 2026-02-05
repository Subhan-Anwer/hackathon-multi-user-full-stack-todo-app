from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    """Base model with common fields for Task."""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """
    Task model representing a todo item that belongs to a specific user.

    Attributes:
        id: Primary key, auto-generated
        user_id: Foreign key linking to user, required for user isolation
        title: Task title, required (1-255 chars)
        description: Optional task description (max 1000 chars)
        completed: Boolean indicating completion status, default false
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False)  # Foreign key with index for performance
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(TaskBase):
    """Model for creating new tasks."""
    title: str = Field(min_length=1, max_length=255)
    # user_id will be set from authentication context


class TaskUpdate(SQLModel):
    """Model for updating existing tasks (all fields optional)."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """Model for task responses with all required fields."""
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime