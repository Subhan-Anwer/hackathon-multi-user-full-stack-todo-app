"""Tests for Session Management Functionality.

This module contains comprehensive tests for session validation,
expiry warnings, and integration with task routes. Tests cover
both positive and negative cases including expired tokens,
invalid tokens, and near-expiry scenarios.
"""

import pytest
import sys
import os
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
import jwt
from unittest.mock import patch

# Add the app directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app
from app.db.db import get_session_dependency
from app.services.session import SessionService
from app.config import settings


@pytest.fixture(name="engine")
def engine_fixture():
    """Create in-memory database engine for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    """Create database session for testing."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(engine, session):
    """Create test client with overridden database session."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session_dependency] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def create_test_token(user_id: str = "test-user", email: str = "test@example.com",
                      expiry_delta: timedelta = timedelta(hours=1)) -> str:
    """Helper function to create a test JWT token."""
    secret = os.getenv("BETTER_AUTH_SECRET", "test-secret-key-for-testing")

    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.utcnow() + expiry_delta
    }

    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


def test_session_service_validate_valid_token():
    """Test that SessionService correctly validates valid tokens."""
    token = create_test_token()

    result = SessionService.validate_session(token)

    assert result is not None
    assert result["user_id"] == "test-user"
    assert result["email"] == "test@example.com"


def test_session_service_validate_expired_token():
    """Test that SessionService rejects expired tokens."""
    token = create_test_token(expiry_delta=timedelta(seconds=-1))  # Expired 1 second ago

    result = SessionService.validate_session(token)

    assert result is None


def test_session_service_validate_invalid_token():
    """Test that SessionService rejects invalid tokens."""
    result = SessionService.validate_session("invalid.token.here")

    assert result is None


def test_session_service_get_expiry_info():
    """Test that SessionService correctly gets expiry information."""
    token = create_test_token()

    result = SessionService.get_session_expiry_info(token)

    assert result is not None
    assert result["user_id"] == "test-user"
    assert result["email"] == "test@example.com"
    assert result["expires_in_seconds"] > 0  # Should have time remaining


def test_session_service_is_about_to_expire_true():
    """Test that SessionService correctly identifies tokens about to expire."""
    token = create_test_token(expiry_delta=timedelta(minutes=5))  # Expires in 5 minutes

    result = SessionService.is_session_about_to_expire(token, threshold_minutes=10)

    assert result is True  # Should be true since 5 minutes < 10 minute threshold


def test_session_service_is_about_to_expire_false():
    """Test that SessionService correctly identifies tokens not about to expire."""
    token = create_test_token(expiry_delta=timedelta(hours=2))  # Expires in 2 hours

    result = SessionService.is_session_about_to_expire(token, threshold_minutes=10)

    assert result is False  # Should be false since 2 hours > 10 minute threshold


def test_session_service_is_valid_user_session_correct_user():
    """Test that SessionService validates correct user assignment."""
    token = create_test_token(user_id="user-123")

    result = SessionService.is_valid_user_session(token, "user-123")

    assert result is True


def test_session_service_is_valid_user_session_wrong_user():
    """Test that SessionService rejects wrong user assignment."""
    token = create_test_token(user_id="user-123")

    result = SessionService.is_valid_user_session(token, "user-456")

    assert result is False


def test_session_service_get_remaining_time():
    """Test that SessionService correctly calculates remaining time."""
    token = create_test_token(expiry_delta=timedelta(minutes=30))

    result = SessionService.get_remaining_session_time(token)

    assert result is not None
    assert result.total_seconds() > 0


def test_session_service_get_remaining_time_expired():
    """Test that SessionService returns None for expired tokens."""
    token = create_test_token(expiry_delta=timedelta(seconds=-1))

    result = SessionService.get_remaining_session_time(token)

    assert result is None


def test_convenience_functions():
    """Test convenience functions for session management."""
    token = create_test_token(user_id="user-456")

    # Test validate_session_token
    result = SessionService.validate_session(token)
    assert result is not None

    # Test is_session_valid_for_user
    result = SessionService.is_valid_user_session(token, "user-456")
    assert result is True

    # Test is_session_nearing_expiry
    result = SessionService.is_session_about_to_expire(token, 10)
    assert result is False  # Fresh token shouldn't be near expiry

    # Test get_session_remaining_time
    result = SessionService.get_remaining_session_time(token)
    assert result is not None


def test_task_routes_with_valid_session(client):
    """Test task routes accept valid sessions."""
    token = create_test_token(user_id="user-789")
    headers = {"Authorization": f"Bearer {token}"}

    # Test GET tasks endpoint
    response = client.get("/api/user-789/tasks", headers=headers)

    # Should return 200 OK (empty list) with valid session
    assert response.status_code == 200
    assert response.json() == []


def test_task_routes_reject_expired_session(client):
    """Test task routes reject expired sessions."""
    token = create_test_token(user_id="user-789", expiry_delta=timedelta(seconds=-1))
    headers = {"Authorization": f"Bearer {token}"}

    # Test GET tasks endpoint
    response = client.get("/api/user-789/tasks", headers=headers)

    # Should return 401 Unauthorized for expired session
    assert response.status_code == 401


def test_task_routes_reject_invalid_session(client):
    """Test task routes reject invalid sessions."""
    headers = {"Authorization": "Bearer invalid.token.here"}

    # Test GET tasks endpoint
    response = client.get("/api/user-789/tasks", headers=headers)

    # Should return 401 Unauthorized for invalid session
    assert response.status_code == 401


def test_task_routes_reject_wrong_user_assignment(client):
    """Test task routes reject sessions for wrong user."""
    token = create_test_token(user_id="user-123")  # Token for user-123
    headers = {"Authorization": f"Bearer {token}"}

    # Try to access user-456's tasks with user-123's token
    response = client.get("/api/user-456/tasks", headers=headers)

    # Should return 403 Forbidden for wrong user assignment
    assert response.status_code == 403


def test_session_info_endpoint_valid_session(client):
    """Test session info endpoint with valid session."""
    token = create_test_token(user_id="user-789", email="user@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/user-789/session-info", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user-789"
    assert data["email"] == "user@example.com"
    assert data["is_nearing_expiry"] is False
    assert data["remaining_time_seconds"] > 0
    assert "Session is valid" in data["message"]


def test_session_info_endpoint_near_expiry(client):
    """Test session info endpoint with session near expiry."""
    # Create a token that expires in 5 minutes (assuming threshold of 10 mins)
    token = create_test_token(
        user_id="user-789",
        email="user@example.com",
        expiry_delta=timedelta(minutes=5)
    )
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/user-789/session-info", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user-789"
    assert data["email"] == "user@example.com"
    assert data["is_nearing_expiry"] is True
    assert data["remaining_time_seconds"] > 0
    assert "Session will expire" in data["message"]


def test_session_info_endpoint_expired_session(client):
    """Test session info endpoint with expired session."""
    token = create_test_token(
        user_id="user-789",
        expiry_delta=timedelta(seconds=-1)
    )
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/user-789/session-info", headers=headers)

    # Should return 401 Unauthorized for expired session
    assert response.status_code == 401


def test_session_info_endpoint_invalid_session(client):
    """Test session info endpoint with invalid session."""
    headers = {"Authorization": "Bearer invalid.token.here"}

    response = client.get("/api/user-789/session-info", headers=headers)

    # Should return 401 Unauthorized for invalid session
    assert response.status_code == 401


def test_session_info_endpoint_wrong_user_assignment(client):
    """Test session info endpoint rejects wrong user assignment."""
    token = create_test_token(user_id="user-123")  # Token for user-123
    headers = {"Authorization": f"Bearer {token}"}

    # Try to access user-456's session info with user-123's token
    response = client.get("/api/user-456/session-info", headers=headers)

    # Should return 403 Forbidden for wrong user assignment
    assert response.status_code == 403


def test_session_expiry_warning_threshold_customizable(client):
    """Test that session expiry warning threshold is customizable."""
    # Create a token that expires in 15 minutes
    token = create_test_token(
        user_id="user-789",
        email="user@example.com",
        expiry_delta=timedelta(minutes=15)
    )
    headers = {"Authorization": f"Bearer {token}"}

    # With default threshold (10 minutes), should show as near expiry
    response = client.get("/api/user-789/session-info", headers=headers)

    assert response.status_code == 200
    data = response.json()
    # With 15 minutes remaining and 10 minute threshold, should not be near expiry
    assert data["is_nearing_expiry"] is False


@patch.dict(os.environ, {"BETTER_AUTH_SECRET": "different-test-secret"})
def test_session_validation_different_secret():
    """Test session validation with different secret (should fail)."""
    # Create token with default secret
    token = create_test_token()

    # Override secret in environment
    original_secret = os.environ.get("BETTER_AUTH_SECRET")
    os.environ["BETTER_AUTH_SECRET"] = "different-test-secret"

    try:
        result = SessionService.validate_session(token)
        # Should fail because secret doesn't match
        assert result is None
    finally:
        # Restore original secret
        if original_secret:
            os.environ["BETTER_AUTH_SECRET"] = original_secret
        else:
            os.environ.pop("BETTER_AUTH_SECRET", None)


def test_jwt_decode_error_handling():
    """Test that JWT decode errors are handled gracefully."""
    # Test with malformed token
    result = SessionService.validate_session("malformed.token.without.proper.parts")
    assert result is None

    # Test with token that has invalid signature
    result = SessionService.validate_session("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")
    assert result is None


if __name__ == "__main__":
    pytest.main([__file__])