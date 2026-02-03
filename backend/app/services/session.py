"""Session Management Service for User Sessions.

This module provides functions to handle user sessions, including validation,
refresh, and cleanup. It works with Better Auth's session management system
to maintain secure and efficient user sessions.
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict
import jwt
from sqlmodel import Session, select
from ..models.models import Task
from ..config import settings


class SessionService:
    """Service class for managing user sessions."""

    @staticmethod
    def validate_session(token: str) -> Optional[Dict[str, str]]:
        """
        Validate a JWT session token.

        Args:
            token: JWT token to validate

        Returns:
            User information dictionary if valid, None if invalid/expired
        """
        try:
            payload = jwt.decode(
                token,
                settings.BETTER_AUTH_SECRET,
                algorithms=["HS256"],
                options={"verify_signature": True}
            )

            # Check if token is expired
            exp_time = datetime.fromtimestamp(payload.get("exp", 0))
            if exp_time < datetime.utcnow():
                return None

            return {
                "user_id": payload.get("sub"),
                "email": payload.get("email"),
                "exp": payload.get("exp")
            }
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def get_session_expiry_info(token: str) -> Optional[Dict[str, any]]:
        """
        Get session expiry information without validating the signature.

        Args:
            token: JWT token to inspect

        Returns:
            Dictionary with expiry info if token is validly formatted, None otherwise
        """
        try:
            # Decode without verification to get expiry info
            payload = jwt.decode(
                token,
                options={"verify_signature": False}
            )

            exp_timestamp = payload.get("exp", 0)
            exp_datetime = datetime.fromtimestamp(exp_timestamp) if exp_timestamp else None

            return {
                "exp": exp_datetime,
                "expires_in_seconds": (exp_datetime - datetime.utcnow()).total_seconds() if exp_datetime else 0,
                "user_id": payload.get("sub"),
                "email": payload.get("email")
            }
        except jwt.DecodeError:
            return None

    @staticmethod
    def is_session_about_to_expire(token: str, threshold_minutes: int = 10) -> bool:
        """
        Check if session is about to expire within the threshold.

        Args:
            token: JWT token to check
            threshold_minutes: Minutes before expiry to consider as "about to expire"

        Returns:
            True if session expires within threshold, False otherwise
        """
        expiry_info = SessionService.get_session_expiry_info(token)
        if not expiry_info or not expiry_info["exp"]:
            return True  # Consider invalid tokens as needing refresh

        seconds_until_expiry = expiry_info["expires_in_seconds"]
        return seconds_until_expiry <= (threshold_minutes * 60)

    @staticmethod
    def get_remaining_session_time(token: str) -> Optional[timedelta]:
        """
        Get the remaining time before session expires.

        Args:
            token: JWT token to check

        Returns:
            Timedelta representing remaining time, None if invalid
        """
        expiry_info = SessionService.get_session_expiry_info(token)
        if not expiry_info or not expiry_info["exp"]:
            return None

        return timedelta(seconds=expiry_info["expires_in_seconds"])

    @staticmethod
    def is_valid_user_session(token: str, expected_user_id: str) -> bool:
        """
        Validate that a session token belongs to the expected user.

        Args:
            token: JWT token to validate
            expected_user_id: User ID that should match the token's subject

        Returns:
            True if session is valid and belongs to expected user, False otherwise
        """
        session_info = SessionService.validate_session(token)
        if not session_info:
            return False

        return session_info.get("user_id") == expected_user_id


# Convenience functions for common session operations
def validate_session_token(token: str) -> Optional[Dict[str, str]]:
    """Convenience function to validate a session token."""
    return SessionService.validate_session(token)


def is_session_valid_for_user(token: str, user_id: str) -> bool:
    """Convenience function to validate session for a specific user."""
    return SessionService.is_valid_user_session(token, user_id)


def is_session_nearing_expiry(token: str, threshold_minutes: int = 10) -> bool:
    """Convenience function to check if session is nearing expiry."""
    return SessionService.is_session_about_to_expire(token, threshold_minutes)


def get_session_remaining_time(token: str) -> Optional[timedelta]:
    """Convenience function to get remaining session time."""
    return SessionService.get_remaining_session_time(token)