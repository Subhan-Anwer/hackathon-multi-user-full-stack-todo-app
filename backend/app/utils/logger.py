"""
Backend Authentication Logger

Provides structured JSON logging for authentication events on the backend.
Logs are written to console and can be configured to write to files.
"""

import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'  # We'll format as JSON manually
)

logger = logging.getLogger(__name__)


class AuthLogger:
    """
    Backend authentication logger for JWT verification and session management.

    Logs structured JSON events for:
    - Token validation (success/failure)
    - Session checks
    - User authorization checks
    - Authentication errors
    """

    def __init__(self, log_to_file: bool = False, log_dir: Optional[Path] = None):
        """
        Initialize the authentication logger.

        Args:
            log_to_file: If True, also write logs to file
            log_dir: Directory for log files (default: backend/logs/)
        """
        self.log_to_file = log_to_file
        self.log_dir = log_dir or Path(__file__).parent.parent.parent / "logs"

        if self.log_to_file:
            self.log_dir.mkdir(exist_ok=True)

    def _log_event(self, event: Dict[str, Any]) -> None:
        """
        Log a structured authentication event.

        Args:
            event: Dictionary containing event data
        """
        # Add timestamp if not present
        if "timestamp" not in event:
            event["timestamp"] = datetime.utcnow().isoformat() + "Z"

        # Log to console as JSON
        log_entry = json.dumps(event)
        logger.info(log_entry)

        # Optionally log to file
        if self.log_to_file:
            log_file = self.log_dir / f"auth-{datetime.utcnow().strftime('%Y-%m-%d')}.log"
            with open(log_file, "a") as f:
                f.write(log_entry + "\n")

    def token_validation_success(self, user_id: str, email: Optional[str] = None) -> None:
        """
        Log successful JWT token validation.

        Args:
            user_id: ID of the authenticated user
            email: Email of the authenticated user
        """
        self._log_event({
            "event": "token_validation_success",
            "user_id": user_id,
            "email": email,
            "success": True,
        })

    def token_validation_failure(self, reason: str, token_preview: Optional[str] = None) -> None:
        """
        Log failed JWT token validation.

        Args:
            reason: Reason for validation failure
            token_preview: First 10 chars of token (for debugging)
        """
        self._log_event({
            "event": "token_validation_failure",
            "reason": reason,
            "token_preview": token_preview,
            "success": False,
        })

    def session_check(self, user_id: str, is_valid: bool, endpoint: Optional[str] = None) -> None:
        """
        Log session validation check.

        Args:
            user_id: ID of the user being checked
            is_valid: Whether the session is valid
            endpoint: API endpoint being accessed
        """
        self._log_event({
            "event": "session_check",
            "user_id": user_id,
            "is_valid": is_valid,
            "endpoint": endpoint,
            "success": is_valid,
        })

    def authorization_check(
        self,
        user_id: str,
        requested_user_id: str,
        is_authorized: bool,
        endpoint: Optional[str] = None
    ) -> None:
        """
        Log user authorization check (user isolation).

        Args:
            user_id: ID of authenticated user
            requested_user_id: ID in the URL being accessed
            is_authorized: Whether access is authorized
            endpoint: API endpoint being accessed
        """
        self._log_event({
            "event": "authorization_check",
            "user_id": user_id,
            "requested_user_id": requested_user_id,
            "is_authorized": is_authorized,
            "endpoint": endpoint,
            "success": is_authorized,
        })

    def missing_token(self, endpoint: Optional[str] = None) -> None:
        """
        Log missing authentication token.

        Args:
            endpoint: API endpoint that was accessed
        """
        self._log_event({
            "event": "missing_token",
            "endpoint": endpoint,
            "success": False,
            "reason": "No Authorization header provided",
        })

    def expired_token(self, user_id: Optional[str] = None, endpoint: Optional[str] = None) -> None:
        """
        Log expired token detection.

        Args:
            user_id: ID from expired token (if decodable)
            endpoint: API endpoint that was accessed
        """
        self._log_event({
            "event": "expired_token",
            "user_id": user_id,
            "endpoint": endpoint,
            "success": False,
            "reason": "Token has expired",
        })

    def invalid_token_format(self, token_preview: Optional[str] = None) -> None:
        """
        Log invalid token format.

        Args:
            token_preview: First 10 chars of token (for debugging)
        """
        self._log_event({
            "event": "invalid_token_format",
            "token_preview": token_preview,
            "success": False,
            "reason": "Token format is invalid",
        })


# Global auth logger instance
auth_logger = AuthLogger()
