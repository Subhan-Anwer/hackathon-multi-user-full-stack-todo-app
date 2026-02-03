from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime, String, Boolean, Index, event
from sqlalchemy.sql import func


class Task(SQLModel, table=True):
    """
    Task model representing a todo item created by a user.

    Contains title, description, completion status, and timestamps.
    Enforces user isolation through user_id foreign key relationship.
    """

    __tablename__ = "tasks"

    # Define table indexes for performance
    __table_args__ = (
        Index('idx_user_id', 'user_id'),  # Index on user_id for efficient queries
        Index('idx_completed', 'completed'),  # Index on completed status
        Index('idx_user_completed', 'user_id', 'completed'),  # Composite index for combined queries
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        max_length=255,
        nullable=False,
        index=True
    )  # Foreign key reference to users.id with cascade delete handled at DB level (constraint handled at DB level)
    title: str = Field(
        max_length=200,
        nullable=False
    )  # Max 200 characters as per requirements
    description: Optional[str] = Field(
        max_length=1000,
        default=None
    )  # Max 1000 characters, nullable as per requirements
    completed: bool = Field(
        default=False,
        nullable=False
    )  # Default to False
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"server_default": func.current_timestamp()}
    )  # Auto-populated on creation
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": func.current_timestamp()}
    )  # Auto-populated on creation and updates