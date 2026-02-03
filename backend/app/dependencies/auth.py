"""JWT Authentication Dependencies for FastAPI.

This module provides dependency functions for verifying JWT tokens
and ensuring user isolation in API endpoints.
"""

import os
from typing import Dict
from fastapi import Header, HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError


def get_current_user_id(authorization: str = Header(...)) -> str:
    """
    Extract and verify JWT token from Authorization header.

    Args:
        authorization: Authorization header value (format: "Bearer <token>")

    Returns:
        User ID extracted from token's 'sub' claim

    Raises:
        HTTPException: 401 if token is missing, invalid, or expired
    """
    # Extract token from "Bearer <token>" format
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected 'Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.replace("Bearer ", "").strip()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Verify and decode JWT token
        secret = os.getenv("BETTER_AUTH_SECRET")
        if not secret:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server configuration error: BETTER_AUTH_SECRET not set",
            )

        payload: Dict = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            options={"verify_signature": True}
        )

        # Extract user_id from 'sub' claim (JWT standard)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing 'sub' claim (user ID)",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_user_id_match(url_user_id: str, token_user_id: str) -> None:
    """
    Verify that the user_id in the URL matches the authenticated user's ID.

    This enforces user data isolation by ensuring users can only access
    their own resources.

    Args:
        url_user_id: User ID from the URL path parameter
        token_user_id: User ID extracted from JWT token

    Raises:
        HTTPException: 403 if user IDs don't match (authorization failure)
    """
    if url_user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )


async def get_current_user(authorization: str = Header(...)) -> Dict[str, str]:
    """
    Get current authenticated user information.

    Convenience dependency that returns user data as a dictionary.

    Args:
        authorization: Authorization header value

    Returns:
        Dictionary with user_id and other token claims
    """
    user_id = get_current_user_id(authorization)
    return {"user_id": user_id}