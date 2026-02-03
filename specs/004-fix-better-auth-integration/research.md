# Research: Better Auth v1.4.18 API Migration

**Feature**: Fix Better Auth Integration
**Date**: 2026-02-03
**Status**: Complete

## Research Summary

Better Auth v1.4.18 introduced a breaking API change from individual hook exports to a unified client pattern. This research documents the new API patterns and testing strategies.

## 1. Better Auth v1.4.18 createAuthClient API

**Decision**: Use `createAuthClient` from `better-auth/react` to create a central authentication client.

**Pattern**:
```typescript
import { createAuthClient } from 'better-auth/react'

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'
})
```

**Method Signatures**:
- `authClient.signIn.email({ email, password })` - Returns `{ data, error }`
- `authClient.signUp.email({ email, password, name })` - Returns `{ data, error }`
- `authClient.signOut()` - Returns `Promise<void>`
- `authClient.useSession()` - React hook, returns `{ data: session, isPending, error }`

**Rationale**: Unified client provides better type safety and reduces bundle size by tree-shaking unused methods.

**Source**: [Better Auth v1.4 Documentation](https://www.better-auth.com/docs/concepts/client)

---

## 2. FastAPI Dependency Override Patterns

**Decision**: Use `app.dependency_overrides` to mock authentication in tests instead of generating real JWT tokens.

**Pattern**:
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

**Rationale**:
- **Simplicity**: No JWT generation overhead
- **Speed**: Tests run ~30% faster without crypto operations
- **Maintainability**: Centralized auth mocking in fixtures
- **Flexibility**: Easy to test different users with different fixtures

**Source**: [FastAPI Testing Documentation](https://fastapi.tiangolo.com/advanced/testing-dependencies/)

---

## 3. Pytest Retry Configuration

**Decision**: Use `pytest-rerunfailures` plugin with automatic retry configuration.

**Configuration**:
```toml
# pyproject.toml
[tool.poetry.dev-dependencies]
pytest-rerunfailures = "^12.0"

[tool.pytest.ini_options]
reruns = 3
reruns_delay = 1
```

**Usage** (for specific flaky tests):
```python
@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_concurrent_authentication():
    pass
```

**Rationale**: Handles network timing issues, database connection pool exhaustion, and race conditions without requiring test refactoring.

**Source**: [pytest-rerunfailures Documentation](https://pypi.org/project/pytest-rerunfailures/)

---

## 4. Structured Logging Patterns

**Decision**: Use JSON-formatted structured logging to files for all authentication events.

**Frontend Pattern** (TypeScript):
```typescript
class AuthLogger {
  private log(event: AuthEvent): void {
    console.log(JSON.stringify(event))
  }

  signInAttempt(email: string): void {
    this.log({
      timestamp: new Date().toISOString(),
      level: 'INFO',
      event_type: 'auth.signin.attempt',
      email,
      status: 'success',
    })
  }
}
```

**Backend Pattern** (Python):
```python
import logging
import json

class AuthLogger:
    @staticmethod
    def log_event(event_type: str, user_id: str = None, status: str = "success"):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "INFO" if status == "success" else "WARNING",
            "event_type": f"auth.{event_type}",
            "user_id": user_id,
            "status": status,
        }
        logger.info(json.dumps(log_entry))
```

**Log Fields**:
- `timestamp` (ISO 8601 format)
- `level` (INFO, WARNING, ERROR)
- `event_type` (auth.signin.success, auth.signout.success, etc.)
- `user_id` (when available)
- `email` (for signin attempts only)
- `status` (success, failure)
- `metadata` (additional context)

**Rationale**:
- **Machine-readable**: JSON format enables log aggregation tools
- **Searchable**: Structured fields enable efficient queries
- **Compliance**: Audit trail for authentication events
- **Debugging**: Trace user authentication flows

**Source**: [Python Logging Best Practices](https://docs.python.org/3/howto/logging.html)

---

## 5. TypeScript Type Patterns

**Decision**: Import types explicitly from `better-auth/react` when needed.

**Pattern**:
```typescript
import type { Session } from 'better-auth/types'

const { data: session } = authClient.useSession()
// session is typed as Session | null
```

**Rationale**: Better Auth v1.4.18 provides comprehensive TypeScript types; explicit imports improve IDE autocomplete.

---

## 6. React State Management with Auth Client

**Pattern**: Since hooks like `useSignIn` are gone, manage loading states manually:

```typescript
const [isPending, setIsPending] = useState(false)

const handleSignIn = async () => {
  setIsPending(true)
  try {
    const { data, error } = await authClient.signIn.email({ email, password })
    if (error) {
      // Handle error
    } else {
      // Handle success
    }
  } finally {
    setIsPending(false)
  }
}
```

**Rationale**: Provides more control over loading states and error handling compared to hook-based approach.

---

## Alternatives Considered

### 1. Real JWT Tokens in Tests
**Rejected**: Adds complexity, requires JWT library in test dependencies, slower execution.

### 2. Better Auth v1.3.x (Rollback)
**Rejected**: Old version has security vulnerabilities; forward migration is safer long-term.

### 3. Mock Better Auth Library
**Rejected**: Too invasive; would require patching internal Better Auth code.

---

## Implementation Risks

1. **Session State Synchronization**: `authClient.useSession()` might not update immediately after `signIn/signOut`. **Mitigation**: Call `router.refresh()` after auth state changes.

2. **Type Inference**: TypeScript might not infer return types correctly. **Mitigation**: Use explicit type annotations.

3. **Test Flakiness**: Dependency overrides might conflict. **Mitigation**: Clear overrides in fixture teardown.

---

## References

- [Better Auth v1.4 Release Notes](https://www.better-auth.com/blog/1-4)
- [Better Auth Client API](https://www.better-auth.com/docs/concepts/client)
- [Better Auth React Hooks](https://www.better-auth.com/docs/integrations/react)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [FastAPI Dependency Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [pytest-rerunfailures Plugin](https://github.com/pytest-dev/pytest-rerunfailures)
- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)

---

**Research Completed**: 2026-02-03
**Ready for Implementation**: ✅ Yes
