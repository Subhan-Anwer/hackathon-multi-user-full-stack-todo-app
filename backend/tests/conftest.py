import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.db.db import get_session_dependency
from app.dependencies.auth import get_current_user_id
from app.middleware.auth import JWTMiddleware


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


@pytest.fixture(name="mock_user_id")
def mock_user_id_fixture():
    """Default authenticated user for tests."""
    return "user-123"


@pytest.fixture(name="client")
def client_fixture(session: Session, mock_user_id: str):
    """Create test client with mocked auth and database."""
    # Remove JWT middleware for testing to allow dependency overrides
    middleware_list = []
    for item in app.user_middleware:
        if item.cls != JWTMiddleware:
            middleware_list.append(item)

    # Temporarily replace middleware
    original_middleware = app.user_middleware
    app.user_middleware = middleware_list
    # Rebuild middleware stack
    app.middleware_stack = app.build_middleware_stack()

    def get_session_override():
        return session

    def get_current_user_id_override(authorization: str = "Bearer test-token"):
        # Mock function that accepts the header parameter but returns a hardcoded user ID
        # The header dependency is satisfied but we return a mock user ID
        return mock_user_id

    app.dependency_overrides[get_session_dependency] = get_session_override
    app.dependency_overrides[get_current_user_id] = get_current_user_id_override

    client = TestClient(app)
    yield client

    # Restore original middleware
    app.user_middleware = original_middleware
    app.middleware_stack = app.build_middleware_stack()
    app.dependency_overrides.clear()


@pytest.fixture(name="client_user_456")
def client_user_456_fixture(session: Session):
    """Create test client authenticated as user-456 for cross-user testing."""
    def get_session_override():
        return session

    def get_current_user_id_override(authorization: str = "Bearer test-token"):
        return "user-456"

    app.dependency_overrides[get_session_dependency] = get_session_override
    app.dependency_overrides[get_current_user_id] = get_current_user_id_override

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()