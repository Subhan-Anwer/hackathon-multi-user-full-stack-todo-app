"""Database session dependency for FastAPI.

This module provides dependency functions for database session management.
"""

from sqlmodel import Session
from fastapi import Depends
from ..db.db import get_session_dependency


def get_session() -> Session:
    """Get database session dependency for FastAPI endpoints.

    This dependency handles session creation and cleanup automatically.
    It yields a database session that can be injected into route handlers.

    Yields:
        Session: Database session for executing queries
    """
    with next(get_session_dependency()) as session:
        yield session