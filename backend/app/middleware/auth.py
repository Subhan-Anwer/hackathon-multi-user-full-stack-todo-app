"""JWT Authentication Middleware for FastAPI.

This middleware verifies JWT tokens from Better Auth and attaches
user information to the request state for use in route handlers.
"""

import jwt
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from ..config import settings


class JWTMiddleware(BaseHTTPMiddleware):
    """Middleware to verify JWT tokens on protected routes."""

    async def dispatch(self, request: Request, call_next):
        # Skip auth for public routes
        if request.url.path in ["/docs", "/redoc", "/openapi.json", "/health", "/"]:
            return await call_next(request)

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header"
            )

        token = auth_header.split(" ")[1]

        try:
            # Verify and decode JWT
            payload = jwt.decode(
                token,
                settings.BETTER_AUTH_SECRET,
                algorithms=["HS256"]
            )

            # Attach user info to request state
            request.state.user = {
                "user_id": payload.get("sub"),  # User ID from 'sub' claim
                "email": payload.get("email"),
            }

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        response = await call_next(request)
        return response


def get_current_user(request: Request) -> dict:
    """Extract current user from request state."""
    if not hasattr(request.state, "user"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return request.state.user


