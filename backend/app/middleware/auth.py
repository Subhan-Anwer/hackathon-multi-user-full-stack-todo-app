"""JWT Authentication Middleware for FastAPI.

This middleware verifies JWT tokens from Better Auth and attaches
user information to the request state for use in route handlers.
"""

import jwt
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from ..config import settings
from ..utils.logger import auth_logger


class JWTMiddleware(BaseHTTPMiddleware):
    """Middleware to verify JWT tokens on protected routes."""

    async def dispatch(self, request: Request, call_next):
        # Skip auth for public routes
        if request.url.path in ["/docs", "/redoc", "/openapi.json", "/health", "/"]:
            return await call_next(request)

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            auth_logger.missing_token(endpoint=request.url.path)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header"
            )

        token = auth_header.split(" ")[1]
        token_preview = token[:10] if len(token) >= 10 else token

        try:
            # Verify and decode JWT
            payload = jwt.decode(
                token,
                settings.BETTER_AUTH_SECRET,
                algorithms=["HS256"]
            )

            # Attach user info to request state
            user_id = payload.get("sub")
            email = payload.get("email")
            request.state.user = {
                "user_id": user_id,  # User ID from 'sub' claim
                "email": email,
            }

            # Log successful validation
            auth_logger.token_validation_success(user_id=user_id, email=email)

        except jwt.ExpiredSignatureError:
            # Try to decode without verification to get user_id for logging
            try:
                unverified = jwt.decode(token, options={"verify_signature": False})
                user_id = unverified.get("sub")
            except:
                user_id = None

            auth_logger.expired_token(user_id=user_id, endpoint=request.url.path)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError as e:
            auth_logger.token_validation_failure(
                reason=str(e),
                token_preview=token_preview
            )
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


