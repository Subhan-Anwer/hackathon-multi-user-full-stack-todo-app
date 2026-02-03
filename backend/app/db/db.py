from sqlmodel import create_engine, Session, SQLModel
from contextlib import contextmanager
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True to log SQL queries
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections after 5 minutes
)


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Get database session with automatic cleanup."""
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


# FastAPI dependency
def get_session_dependency() -> Session:
    """FastAPI dependency to get database session."""
    with Session(engine) as session:
        yield session