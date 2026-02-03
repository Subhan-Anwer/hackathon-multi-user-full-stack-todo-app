"""Application configuration for the backend."""

import os
from typing import List, Optional
from datetime import timedelta


class Settings:
    """Application settings from environment variables."""

    def __init__(self):
        # Database settings
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "")

        # Authentication settings
        self.BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "fallback-secret-for-testing")

        # Session management settings
        self.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
        self.REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
        self.SESSION_WARNING_THRESHOLD_MINUTES: int = int(os.getenv("SESSION_WARNING_THRESHOLD_MINUTES", "10"))

        # CORS settings
        self.CORS_ORIGINS: List[str] = self._parse_cors_origins(os.getenv("CORS_ORIGINS", "http://localhost:3000"))

        # Debug settings
        self.DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

        # Security settings
        self.JWT_LEEWAY_SECONDS: int = int(os.getenv("JWT_LEEWAY_SECONDS", "10"))
        self.ALLOWED_CLOCK_SKEW_SECONDS: int = int(os.getenv("ALLOWED_CLOCK_SKEW_SECONDS", "30"))

    def _parse_cors_origins(self, cors_origins_str: str) -> List[str]:
        """Parse CORS origins from environment variable."""
        if cors_origins_str.startswith("[") and cors_origins_str.endswith("]"):
            # Handle JSON-like array format
            import json
            try:
                return json.loads(cors_origins_str)
            except json.JSONDecodeError:
                pass

        # Handle comma-separated format
        return [origin.strip() for origin in cors_origins_str.split(",")]

    @property
    def access_token_expire_delta(self) -> timedelta:
        """Get access token expiration as timedelta."""
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

    @property
    def refresh_token_expire_delta(self) -> timedelta:
        """Get refresh token expiration as timedelta."""
        return timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)

    @property
    def session_warning_threshold_delta(self) -> timedelta:
        """Get session warning threshold as timedelta."""
        return timedelta(minutes=self.SESSION_WARNING_THRESHOLD_MINUTES)


# Create settings instance
settings = Settings()