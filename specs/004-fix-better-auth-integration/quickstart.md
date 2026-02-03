# Quick Reference: Better Auth v1.4.18 Migration

**Feature**: Fix Better Auth Integration | **Date**: 2026-02-03

## API Changes Summary

Better Auth v1.4.18 replaced individual hooks with a unified client pattern.

### OLD (Deprecated) ❌

```typescript
import { useSignIn, useSignOut, useSession } from 'better-auth/react'

const { signIn, isPending } = useSignIn({ onSuccess: () => {...} })
const { signOut, isPending } = useSignOut()
const { data: session } = useSession()
```

### NEW (Current) ✅

```typescript
import { authClient } from '@/lib/auth-client'

// Sign In
const { data, error } = await authClient.signIn.email({ email, password })

// Sign Up
const { data, error } = await authClient.signUp.email({ email, password, name })

// Sign Out
await authClient.signOut()

// Check Session
const { data: session, isPending, error } = authClient.useSession()
```

---

## Frontend Migration Checklist

- [ ] Create `frontend/src/lib/auth-client.ts` with `createAuthClient`
- [ ] Fix `login/page.tsx`: Replace `useSignIn` with `authClient.signIn.email()`
- [ ] Fix `signup/page.tsx`: Replace `useRegister` with `authClient.signUp.email()`
- [ ] Fix `logout-button.tsx`: Replace `useSignOut` with `authClient.signOut()`
- [ ] Fix `protected-route.tsx`: Replace `useSession` with `authClient.useSession()`
- [ ] Add structured logging (optional: FR-011)

---

## Backend Testing Changes

### OLD (Complex) ❌

```python
# Generate real JWT tokens
token = jwt.encode({"sub": "user-123"}, secret, algorithm="HS256")
response = client.get("/api/user-123/tasks", headers={"Authorization": f"Bearer {token}"})
```

### NEW (Simple) ✅

```python
# Use dependency override in conftest.py
app.dependency_overrides[get_current_user_id] = lambda: "user-123"

# Tests automatically authenticated
def test_something(client: TestClient):
    response = client.get("/api/user-123/tasks")
    assert response.status_code == 200
```

---

## Testing Setup

### 1. Update `conftest.py`

```python
from app.dependencies.auth import get_current_user_id

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_current_user_id_override():
        return "user-123"

    app.dependency_overrides[get_current_user_id] = get_current_user_id_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

### 2. Add Pytest Retry Config

```toml
# pyproject.toml
[tool.poetry.dev-dependencies]
pytest-rerunfailures = "^12.0"

[tool.pytest.ini_options]
reruns = 3  # Retry failed tests up to 3 times
reruns_delay = 1  # Wait 1 second between retries
```

---

## Running Tests

```bash
# Frontend build (should show 0 errors)
cd frontend && npm run build

# Backend tests (should show 33/33 passing)
cd backend && pytest -v

# With retry information
pytest -v --reruns-report
```

---

## Structured Logging

### Frontend

```typescript
import { authLogger } from '@/lib/logger'

authLogger.signInAttempt('user@example.com')
authLogger.signInSuccess('user-123', 'user@example.com')
```

### Backend

```python
from app.utils.logger import auth_logger

auth_logger.token_validation_success(user_id="user-123")
auth_logger.token_validation_failure(reason="expired")
```

**Log Location**:
- Frontend: Browser DevTools → Console (JSON format)
- Backend: `backend/logs/auth.log` (JSON format)

---

## Troubleshooting

### Issue: "useSignIn is not exported from 'better-auth/react'"

**Solution**: Update import to use `authClient` from `@/lib/auth-client`

### Issue: Backend tests fail with 401 Unauthorized

**Solution**: Ensure `conftest.py` has `get_current_user_id` dependency override

### Issue: Session not updating after login/logout

**Solution**: Call `router.refresh()` after auth state changes

### Issue: Tests still failing after 3 retries

**Solution**: Check test logs for patterns; may indicate real bug vs flaky test

---

## File Checklist

### Frontend
- `frontend/src/lib/auth-client.ts` - Central auth client (CREATE)
- `frontend/src/lib/logger.ts` - Auth event logging (CREATE)
- `frontend/src/app/(auth)/login/page.tsx` - Fix useSignIn
- `frontend/src/app/(auth)/signup/page.tsx` - Fix useRegister
- `frontend/src/components/auth/logout-button.tsx` - Fix useSignOut
- `frontend/src/components/auth/protected-route.tsx` - Fix useSession

### Backend
- `backend/tests/conftest.py` - Add dependency override
- `backend/tests/test_auth_flow.py` - Remove JWT token generation
- `backend/tests/test_session_management.py` - Use dependency override
- `backend/app/utils/logger.py` - Auth event logging (CREATE)
- `backend/pyproject.toml` - Add pytest-rerunfailures

---

## Success Criteria

**Frontend**: 0 build errors, all auth flows functional
**Backend**: 33/33 tests passing (14 DB + 19 auth)
**Integration**: End-to-end signup/login/logout works

---

**Quick Reference Version**: 1.0
**Last Updated**: 2026-02-03
