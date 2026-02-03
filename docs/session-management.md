# Session Management Documentation

## Overview

This document describes the session management system implemented in the multi-user todo application. The system provides secure, scalable user sessions using JWT tokens with proper validation, expiry warnings, and user isolation.

## Architecture

### Components

1. **Session Service** (`backend/app/services/session.py`)
   - Core session management functions
   - Token validation and expiry checking
   - Session state management

2. **Authentication Dependencies** (`backend/app/dependencies/auth.py`)
   - Session validation dependencies for FastAPI
   - User ID matching and validation
   - Session expiry warnings

3. **Task Routes** (`backend/app/routes/tasks.py`)
   - Integration with session validation
   - Session info endpoint

4. **Configuration** (`backend/app/config.py`)
   - Session-related settings and parameters

### Session Flow

```
1. User authenticates via Better Auth
2. JWT token issued with configurable expiry
3. Token validated on each API request
4. Session expiry checked and warned
5. User isolation enforced on all operations
6. Session refreshed as needed
```

## Configuration Options

The session management system is configured through environment variables:

| Variable | Description | Default | Type |
|----------|-------------|---------|------|
| `BETTER_AUTH_SECRET` | Secret key for JWT signing/verification | `fallback-secret-for-testing` | String |
| `JWT_ALGORITHM` | Algorithm for JWT signing | `HS256` | String |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiry in minutes | `60` | Integer |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiry in days | `7` | Integer |
| `SESSION_WARNING_THRESHOLD_MINUTES` | Threshold for expiry warnings | `10` | Integer |
| `JWT_LEEWAY_SECONDS` | Allowed leeway for JWT time validation | `10` | Integer |
| `ALLOWED_CLOCK_SKEW_SECONDS` | Clock skew tolerance | `30` | Integer |

## API Endpoints

### Session Information

#### `GET /api/{user_id}/session-info`

Returns session information including expiry status and warnings.

**Headers:**
- `Authorization: Bearer <token>`

**Parameters:**
- `user_id`: The authenticated user's ID

**Response:**
```json
{
  "user_id": "user-123",
  "email": "user@example.com",
  "is_nearing_expiry": false,
  "remaining_time_seconds": 3600,
  "threshold_minutes": 10,
  "message": "Session is valid"
}
```

**Status Codes:**
- `200`: Session information retrieved successfully
- `401`: Invalid or expired session
- `403`: User ID mismatch

#### `GET /session/config`

Returns session configuration information.

**Response:**
```json
{
  "access_token_expiry_minutes": 60,
  "refresh_token_expiry_days": 7,
  "session_warning_threshold_minutes": 10,
  "jwt_algorithm": "HS256",
  "debug_mode": false
}
```

### Task Endpoints with Session Validation

All existing task endpoints now include session validation:

- `GET /api/{user_id}/tasks` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{task_id}` - Get specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle completion

## Security Considerations

### User Isolation

- Every database query filters by the authenticated user's ID
- URL user_id must match token's user_id
- Users cannot access other users' data

### Token Validation

- JWT tokens are validated using the configured secret
- Expiry times are strictly enforced
- Invalid tokens result in 401 Unauthorized responses

### Session Expiry Warnings

- Sessions are checked for near-expiry status
- Warning threshold configurable via `SESSION_WARNING_THRESHOLD_MINUTES`
- Frontend can use these warnings to prompt for session refresh

## Session Service Functions

### Core Validation Functions

- `validate_session_token(token)` - Validates JWT token and returns user info
- `is_session_valid_for_user(token, user_id)` - Checks if token belongs to user
- `is_session_nearing_expiry(token, threshold_minutes)` - Checks if session is near expiry
- `get_session_remaining_time(token)` - Gets remaining time until expiry

### Session Service Class

The `SessionService` class provides static methods for all session operations:

```python
# Validate a session token
session_info = SessionService.validate_session(token)

# Check if session is about to expire
is_near_expiry = SessionService.is_session_about_to_expire(token, 10)

# Get remaining session time
remaining_time = SessionService.get_remaining_session_time(token)

# Verify session belongs to specific user
is_valid = SessionService.is_valid_user_session(token, user_id)
```

## Integration Points

### FastAPI Dependencies

The session management integrates with FastAPI through dependency injection:

```python
from app.dependencies.auth import validate_active_session, check_session_expiry_warning

# Validate active session
session_info: Dict[str, str] = Depends(validate_active_session)

# Check session expiry with warning
session_expiry_info: Dict[str, Any] = Depends(check_session_expiry_warning)
```

### Error Handling

- Invalid sessions return HTTP 401 (Unauthorized)
- Session-user mismatches return HTTP 403 (Forbidden)
- Expired sessions return HTTP 401 (Unauthorized)

## Testing

### Test Coverage

The session management system includes comprehensive tests in `backend/tests/test_session_management.py`:

- Session validation tests
- Expiry checking tests
- Invalid token handling
- Near-expiry warnings
- Integration with task routes
- User isolation enforcement

### Running Tests

```bash
cd backend
pytest tests/test_session_management.py
```

## Best Practices

### For Developers

1. **Always validate sessions** - Use the provided dependency functions
2. **Enforce user isolation** - Verify URL user_id matches token user_id
3. **Handle expiry gracefully** - Check session expiry warnings and refresh as needed
4. **Secure token storage** - Never log tokens or store them insecurely
5. **Configure appropriately** - Set environment variables for your deployment

### For Operations

1. **Strong secrets** - Use a strong, randomly generated `BETTER_AUTH_SECRET`
2. **Appropriate expiry times** - Balance security with user experience
3. **Monitor session usage** - Track session validation failures
4. **Environment-specific configs** - Different settings for dev/staging/prod

## Troubleshooting

### Common Issues

**Issue:** "Invalid or expired token" errors
**Solution:** Verify `BETTER_AUTH_SECRET` matches between frontend and backend

**Issue:** Session expiry warnings appearing too frequently
**Solution:** Adjust `SESSION_WARNING_THRESHOLD_MINUTES` environment variable

**Issue:** Users unable to access their tasks
**Solution:** Verify user_id in URL matches the authenticated user's ID

### Debugging

Enable debug mode by setting `DEBUG=true` to get more detailed logging information.

## Future Enhancements

- Session refresh endpoints
- Session activity tracking
- Revocation mechanisms
- Multi-device session management
- Session timeout configuration per user role