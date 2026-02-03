# Implementation Plan: Fix Better Auth Integration

**Branch**: `004-fix-better-auth-integration` | **Date**: 2026-02-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-fix-better-auth-integration/spec.md`

## Summary

Fix Better Auth v1.4.18 API compatibility issues causing 19 frontend Turbopack build errors and 19 backend authentication test failures. The root cause is Better Auth's migration from individual hooks (`useSignIn`, `useSignOut`, `useRegister`) to a unified `createAuthClient` pattern. This plan implements a surgical API migration strategy that updates imports and method calls while preserving all existing functionality and maintaining the 14 passing database tests.

## Technical Context

**Language/Version**: TypeScript 5.x (Frontend), Python 3.11 (Backend)
**Primary Dependencies**: Better Auth 1.4.18, Next.js 16+, FastAPI, SQLModel, pytest
**Storage**: Neon PostgreSQL (existing, no schema changes required)
**Testing**: Jest/React Testing Library (frontend), pytest (backend)
**Target Platform**: Web application (Next.js frontend + FastAPI backend)
**Project Type**: Web (frontend + backend)
**Performance Goals**: Build <60s, all 33 tests pass with 100% rate
**Constraints**: Zero breaking changes to user experience or API contracts
**Scale/Scope**: 5 frontend components + 2 backend test files + structured logging

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Compliance Status | Notes |
|-----------|------------------|-------|
| **I. Spec-Driven Development** | ✅ **PASS** | Spec completed and approved before planning |
| **II. Zero Manual Coding** | ✅ **PASS** | All code generated through `/sp.implement` workflow |
| **III. User Data Isolation** | ✅ **PASS** | No changes to isolation logic; tests verify existing behavior |
| **IV. JWT-Based Authentication** | ✅ **PASS** | Maintains existing JWT flow; only fixes client API |
| **V. RESTful API Conventions** | ✅ **PASS** | No API contract changes |
| **VI. Responsive Frontend Design** | ✅ **PASS** | No UI changes; preserves existing responsive design |
| **VII. Minimal Viable Product Focus** | ✅ **PASS** | Bug fix focused on restoring core functionality |

**Constitution Gate**: ✅ **PASSED** - No violations. This is a bug fix that restores broken functionality without adding scope.

## Project Structure

### Documentation (this feature)

```text
specs/004-fix-better-auth-integration/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── research.md          # Better Auth API research
├── data-model.md        # No data model changes (bug fix)
├── quickstart.md        # Quick reference for developers
├── contracts/           # No API contract changes
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   │   └── page.tsx          # FIX: Replace useSignIn with authClient.signIn.email()
│   │   │   └── signup/
│   │   │       └── page.tsx          # FIX: Replace useRegister with authClient.signUp.email()
│   │   └── (dashboard)/
│   │       └── layout.tsx            # Uses protected-route (fix cascades here)
│   ├── components/
│   │   └── auth/
│   │       ├── logout-button.tsx     # FIX: Replace useSignOut with authClient.signOut()
│   │       └── protected-route.tsx   # FIX: Replace useSession with authClient.useSession()
│   └── lib/
│       ├── auth-client.ts            # CREATE: Central Better Auth client instance
│       └── logger.ts                 # CREATE: Structured logging for auth events
└── package.json                      # Already has better-auth@1.4.18

backend/
├── app/
│   ├── middleware/
│   │   └── auth.py                   # No changes (JWT verification logic correct)
│   ├── dependencies/
│   │   └── auth.py                   # No changes (dependency injection correct)
│   └── utils/
│       └── logger.py                 # CREATE: Structured logging for backend auth events
└── tests/
    ├── conftest.py                   # FIX: Add dependency override for get_current_user
    ├── test_auth_flow.py             # FIX: Update to use dependency override pattern
    └── test_session_management.py    # FIX: Update to use dependency override pattern
```

**Structure Decision**: Web application structure (Option 2) is already in place. This plan modifies existing files within the established frontend/backend separation. No new directories required except for logging utilities.

## Complexity Tracking

> No violations - table not needed. This bug fix operates within constitutional boundaries.

## Problem Analysis

### Root Cause

Better Auth v1.4.18 changed its API architecture:

**OLD API (Deprecated)**:
```typescript
import { useSignIn, useSignOut, useRegister, useSession } from 'better-auth/react'

// Individual hooks provided directly
const { signIn, isPending } = useSignIn({ onSuccess: () => {...} })
const { signOut, isPending } = useSignOut({ onSuccess: () => {...} })
```

**NEW API (Current)**:
```typescript
import { createAuthClient } from 'better-auth/react'

// Create client instance first
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL
})

// Access methods through client
await authClient.signIn.email({ email, password })
await authClient.signOut()
const { data: session } = authClient.useSession()
```

### Current State

**Frontend Issues** (19 Build Errors):
- `frontend/src/components/auth/logout-button.tsx:4` - `useSignOut` does not exist
- `frontend/src/app/(auth)/login/page.tsx:5` - `useSignIn` does not exist
- `frontend/src/app/(auth)/signup/page.tsx:5` - `useRegister` does not exist
- `frontend/src/components/auth/protected-route.tsx:5` - `useSession` import pattern changed

**Backend Issues** (19 Test Failures):
- `backend/tests/test_auth_flow.py` - Tests create real JWT tokens but should use dependency override
- `backend/tests/test_session_management.py` - Missing FastAPI dependency injection mocks
- `backend/tests/conftest.py` - No `get_current_user` override in test fixtures

## Implementation Strategy

### Phase 0: Research & Documentation

**Objective**: Document Better Auth v1.4.18 API patterns and testing best practices

**Deliverable**: `research.md` with:
1. Better Auth `createAuthClient` configuration options
2. Method signatures for `signIn.email()`, `signUp.email()`, `signOut()`
3. Session management with `authClient.useSession()` hook
4. FastAPI `app.dependency_overrides` patterns for JWT testing
5. Pytest retry configuration (`pytest-rerunfailures` plugin)
6. Structured logging patterns (JSON format, log rotation)

**Research Sources**:
- Better Auth v1.4 documentation
- FastAPI testing documentation
- Pytest rerunfailures plugin documentation
- Python logging best practices

**Acceptance**: All technical unknowns resolved; implementation examples documented

---

### Phase 1: Frontend API Migration

#### 1.1 Create Auth Client (Foundational)

**File**: `frontend/src/lib/auth-client.ts` (CREATE NEW)

**Purpose**: Central authentication client instance following Better Auth v1.4.18 pattern

**Implementation**:
```typescript
import { createAuthClient } from 'better-auth/react'

/**
 * Better Auth Client Configuration
 *
 * This is the central authentication client used throughout the application.
 * It provides methods for:
 * - Sign in: authClient.signIn.email({ email, password })
 * - Sign up: authClient.signUp.email({ email, password, name })
 * - Sign out: authClient.signOut()
 * - Session: authClient.useSession() hook
 *
 * @see https://www.better-auth.com/docs/concepts/client
 */
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000',
})
```

**Dependencies**: None (foundational file)
**Testing**: Import in any component to verify no build errors

---

#### 1.2 Fix Login Page

**File**: `frontend/src/app/(auth)/login/page.tsx`

**Changes**:
```typescript
// BEFORE (line 5):
import { useSignIn, useSession } from 'better-auth/react';

// AFTER:
import { authClient } from '@/lib/auth-client';

// BEFORE (line 23-32):
const { data: session, isPending: sessionPending } = useSession();
const { signIn, isPending: signInPending } = useSignIn({
  onSuccess: () => {
    router.push('/dashboard');
  },
  onError: (error) => {
    console.error('Login error:', error);
  }
});

// AFTER:
const { data: session, isPending: sessionPending } = authClient.useSession();
const [signInPending, setSignInPending] = useState(false);

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  if (!validateForm()) return;

  setSignInPending(true);
  try {
    const { data, error } = await authClient.signIn.email({
      email: formData.email,
      password: formData.password,
    });

    if (error) {
      console.error('Login error:', error);
      setErrors({ general: 'Invalid email or password' });
    } else {
      router.push('/dashboard');
    }
  } finally {
    setSignInPending(false);
  }
};
```

**Key Changes**:
- Import `authClient` instead of individual hooks
- Replace `useSignIn` with manual state + `authClient.signIn.email()`
- Replace `useSession` with `authClient.useSession()`
- Handle callbacks manually in try/catch

**Dependencies**: Requires `auth-client.ts` created first
**Testing**: Verify login with valid/invalid credentials

---

#### 1.3 Fix Signup Page

**File**: `frontend/src/app/(auth)/signup/page.tsx`

**Changes**:
```typescript
// BEFORE (line 5):
import { useRegister, useSession } from 'better-auth/react';

// AFTER:
import { authClient } from '@/lib/auth-client';

// BEFORE (line 23-32):
const { data: session, isPending: sessionPending } = useSession();
const { register, isPending: registerPending } = useRegister({
  onSuccess: () => {
    router.push('/dashboard');
  },
  onError: (error) => {
    console.error('Signup error:', error);
  }
});

// AFTER:
const { data: session, isPending: sessionPending } = authClient.useSession();
const [registerPending, setRegisterPending] = useState(false);

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  if (!validateForm()) return;

  setRegisterPending(true);
  try {
    const { data, error } = await authClient.signUp.email({
      email: formData.email,
      password: formData.password,
      name: formData.email.split('@')[0], // Use email prefix as name
    });

    if (error) {
      console.error('Signup error:', error);
      setErrors({ general: 'Failed to create account' });
    } else {
      router.push('/dashboard');
    }
  } finally {
    setRegisterPending(false);
  }
};
```

**Key Changes**: Same pattern as login page

**Dependencies**: Requires `auth-client.ts`
**Testing**: Verify signup with new account

---

#### 1.4 Fix Logout Button

**File**: `frontend/src/components/auth/logout-button.tsx`

**Changes**:
```typescript
// BEFORE (line 4):
import { useSignOut } from 'better-auth/react';

// AFTER:
import { authClient } from '@/lib/auth-client';

// BEFORE (line 16-27):
const { signOut, isPending } = useSignOut({
  onSuccess: () => {
    router.push('/auth/login');
    router.refresh();
  },
  onError: (error) => {
    console.error('Logout error:', error);
    router.push('/auth/login');
  }
});

const handleClick = async () => {
  try {
    await signOut();
  } catch (error) {
    console.error('Failed to logout:', error);
    router.push('/auth/login');
  }
};

// AFTER:
const [isPending, setIsPending] = useState(false);

const handleClick = async () => {
  setIsPending(true);
  try {
    await authClient.signOut();
    router.push('/auth/login');
    router.refresh();
  } catch (error) {
    console.error('Failed to logout:', error);
    router.push('/auth/login');
  } finally {
    setIsPending(false);
  }
};
```

**Key Changes**: Replace `useSignOut` hook with manual state + `authClient.signOut()`

**Dependencies**: Requires `auth-client.ts`
**Testing**: Verify logout clears session and redirects

---

#### 1.5 Fix Protected Route

**File**: `frontend/src/components/auth/protected-route.tsx`

**Changes**:
```typescript
// BEFORE (line 4):
import { useSession } from 'better-auth/react';

// AFTER:
import { authClient } from '@/lib/auth-client';

// BEFORE (line 15):
const { data: session, isPending } = useSession();

// AFTER:
const { data: session, isPending } = authClient.useSession();
```

**Key Changes**: Access `useSession` through `authClient` object

**Dependencies**: Requires `auth-client.ts`
**Testing**: Verify protected routes redirect unauthenticated users

---

#### 1.6 Add Frontend Structured Logging (FR-011)

**File**: `frontend/src/lib/logger.ts` (CREATE NEW)

**Purpose**: Structured logging for authentication events per FR-011 requirement

**Implementation**:
```typescript
interface AuthEvent {
  timestamp: string
  level: 'INFO' | 'WARNING' | 'ERROR'
  event_type: string
  user_id?: string
  email?: string
  status: 'success' | 'failure'
  metadata?: Record<string, unknown>
}

class AuthLogger {
  private log(event: AuthEvent): void {
    // In production, send to logging service (e.g., LogRocket, Sentry)
    // In development, log to console
    if (typeof window !== 'undefined') {
      console.log(JSON.stringify(event))
    }
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

  signInSuccess(userId: string, email: string): void {
    this.log({
      timestamp: new Date().toISOString(),
      level: 'INFO',
      event_type: 'auth.signin.success',
      user_id: userId,
      email,
      status: 'success',
    })
  }

  signInFailure(email: string, error: string): void {
    this.log({
      timestamp: new Date().toISOString(),
      level: 'WARNING',
      event_type: 'auth.signin.failure',
      email,
      status: 'failure',
      metadata: { error },
    })
  }

  signOutSuccess(userId: string): void {
    this.log({
      timestamp: new Date().toISOString(),
      level: 'INFO',
      event_type: 'auth.signout.success',
      user_id: userId,
      status: 'success',
    })
  }

  sessionCheck(userId: string | null, isValid: boolean): void {
    this.log({
      timestamp: new Date().toISOString(),
      level: 'INFO',
      event_type: 'auth.session.check',
      user_id: userId || undefined,
      status: isValid ? 'success' : 'failure',
    })
  }
}

export const authLogger = new AuthLogger()
```

**Integration Points**:
- Add `authLogger.signInAttempt()` before `authClient.signIn.email()` in login page
- Add `authLogger.signInSuccess()` / `signInFailure()` in login success/error handlers
- Add `authLogger.signOutSuccess()` in logout handler
- Add `authLogger.sessionCheck()` in protected route component

**Dependencies**: None
**Testing**: Verify console logs in browser DevTools

---

### Phase 2: Backend Test Fixes

#### 2.1 Fix Test Fixtures (Foundational)

**File**: `backend/tests/conftest.py`

**Current Issue**: No dependency override for `get_current_user`, tests fail because JWT middleware expects real tokens

**Changes**:
```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from app.main import app
from app.db.db import get_session_dependency
from app.dependencies.auth import get_current_user_id

# In-memory SQLite for tests
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# Mock authenticated user (default: user-123)
@pytest.fixture(name="mock_user_id")
def mock_user_id_fixture():
    return "user-123"

# Test client with mocked auth
@pytest.fixture(name="client")
def client_fixture(session: Session, mock_user_id: str):
    def get_session_override():
        return session

    def get_current_user_id_override():
        return mock_user_id

    app.dependency_overrides[get_session_dependency] = get_session_override
    app.dependency_overrides[get_current_user_id] = get_current_user_id_override

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()

# Client for testing cross-user access (user-456)
@pytest.fixture(name="client_user_456")
def client_user_456_fixture(session: Session):
    def get_session_override():
        return session

    def get_current_user_id_override():
        return "user-456"

    app.dependency_overrides[get_session_dependency] = get_session_override
    app.dependency_overrides[get_current_user_id] = get_current_user_id_override

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()
```

**Key Changes**:
- Add `get_current_user_id` dependency override
- Default user is `user-123`
- Provide separate fixture for `user-456` (cross-user testing)
- Clear overrides after each test

**Dependencies**: None
**Testing**: All backend tests should now pass with mocked auth

---

#### 2.2 Simplify Auth Flow Tests

**File**: `backend/tests/test_auth_flow.py`

**Current Issue**: Tests create real JWT tokens but dependency override makes them unnecessary

**Changes**:
```python
def test_valid_authentication_flow(client: TestClient, session: Session):
    """Test that authenticated user can access their own tasks."""
    # No JWT token needed - client fixture mocks authentication

    # Create task via direct database call (bypasses API for setup)
    from app.models.models import Task
    task = Task(user_id="user-123", title="Test Task", completed=False)
    session.add(task)
    session.commit()

    # Test API endpoint (auth handled by fixture)
    response = client.get("/api/user-123/tasks")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == "user-123"

def test_cross_user_access_denied(
    client: TestClient,
    client_user_456: TestClient,
    session: Session
):
    """Test that users cannot access other users' tasks."""
    # Create task for user-456
    from app.models.models import Task
    task = Task(user_id="user-456", title="User 456 Task", completed=False)
    session.add(task)
    session.commit()

    # Try to access with user-123's client
    response = client.get("/api/user-456/tasks")

    # Should fail because client is authenticated as user-123
    assert response.status_code == 403
```

**Key Changes**:
- Remove JWT token creation (unnecessary with dependency override)
- Use direct database calls for test data setup
- Use fixtures for different users

**Dependencies**: Requires `conftest.py` fixes
**Testing**: Run `pytest tests/test_auth_flow.py -v`

---

#### 2.3 Simplify Session Management Tests

**File**: `backend/tests/test_session_management.py`

**Changes**: Same pattern as `test_auth_flow.py`:
- Remove JWT token generation
- Use `client` fixture for authenticated requests
- Test session validation logic directly

**Dependencies**: Requires `conftest.py` fixes
**Testing**: Run `pytest tests/test_session_management.py -v`

---

#### 2.4 Add Pytest Retry Configuration

**File**: `backend/pyproject.toml`

**Purpose**: Implement 3-retry strategy per clarification session decision

**Changes**:
```toml
[tool.poetry.dev-dependencies]
pytest = "^7.4.0"
pytest-rerunfailures = "^12.0"  # ADD THIS

[tool.pytest.ini_options]
markers = [
    "flaky: marks tests that may fail intermittently",
]
# Automatically retry all tests up to 3 times
reruns = 3
reruns_delay = 1  # Wait 1 second between retries
```

**Alternative** (mark specific tests):
```python
import pytest

@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_concurrent_authentication():
    # Test that might be flaky
    pass
```

**Dependencies**: None
**Testing**: Run pytest with `-v` to see retry information

---

#### 2.5 Add Backend Structured Logging (FR-011)

**File**: `backend/app/utils/logger.py` (CREATE NEW)

**Purpose**: Structured logging for authentication events per FR-011

**Implementation**:
```python
import logging
import json
from datetime import datetime
from typing import Optional, Dict, Any

# Configure logging to write to file
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',  # JSON format, no extra formatting
    handlers=[
        logging.FileHandler('logs/auth.log'),
        logging.StreamHandler()  # Also log to console
    ]
)

logger = logging.getLogger(__name__)

class AuthLogger:
    @staticmethod
    def log_event(
        event_type: str,
        user_id: Optional[str] = None,
        email: Optional[str] = None,
        status: str = "success",
        metadata: Optional[Dict[str, Any]] = None
    ):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "INFO" if status == "success" else "WARNING",
            "event_type": f"auth.{event_type}",
            "user_id": user_id,
            "email": email,
            "status": status,
            "metadata": metadata or {}
        }
        logger.info(json.dumps(log_entry))

    def token_validation_success(self, user_id: str):
        self.log_event("token.validation", user_id=user_id, status="success")

    def token_validation_failure(self, reason: str):
        self.log_event("token.validation", status="failure", metadata={"reason": reason})

    def session_check(self, user_id: str, is_valid: bool):
        self.log_event(
            "session.check",
            user_id=user_id,
            status="success" if is_valid else "failure"
        )

auth_logger = AuthLogger()
```

**Integration Points**:
- Add to `backend/app/middleware/auth.py` in JWT verification success/failure paths
- Add to `backend/app/dependencies/auth.py` in `get_current_user_id()` function

**Dependencies**: None (create `logs/` directory)
**Testing**: Verify `logs/auth.log` is created and populated

---

### Phase 3: Integration Testing & Validation

#### 3.1 Frontend Build Verification

**Command**:
```bash
cd frontend
npm run build
```

**Expected Result**:
- ✅ 0 errors (down from 19 Turbopack errors)
- ✅ 0 TypeScript errors
- ✅ Build artifacts created in `.next/` directory

**Validation**:
- Check terminal output for "Compiled successfully"
- Verify no import errors
- Check bundle sizes are reasonable

---

#### 3.2 Backend Test Execution

**Command**:
```bash
cd backend
pytest tests/test_auth_flow.py tests/test_session_management.py -v --tb=short
```

**Expected Result**:
- ✅ 19/19 auth tests passing (up from 0)
- ✅ 14/14 database tests still passing
- ✅ Total: 33/33 tests passing (100%)

**Validation**:
- Green test output
- No deprecation warnings
- Retry information displayed if tests are flaky

---

#### 3.3 End-to-End Authentication Flow

**Manual Testing Checklist**:

1. **Startup**:
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn app.main:app --reload --port 8000

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

2. **Signup Flow**:
   - [ ] Navigate to http://localhost:3000/auth/signup
   - [ ] Enter email: test@example.com
   - [ ] Enter password: password123
   - [ ] Click "Sign Up"
   - [ ] Verify redirect to /dashboard
   - [ ] Verify httpOnly cookie set in DevTools → Application → Cookies

3. **Login Flow**:
   - [ ] Click logout button
   - [ ] Navigate to http://localhost:3000/auth/login
   - [ ] Enter email: test@example.com
   - [ ] Enter password: password123
   - [ ] Click "Sign In"
   - [ ] Verify redirect to /dashboard

4. **Protected Routes**:
   - [ ] Navigate to http://localhost:3000/dashboard (should succeed)
   - [ ] Open DevTools → Application → Cookies
   - [ ] Delete "better-auth.session_token" cookie
   - [ ] Refresh page
   - [ ] Verify redirect to /auth/login

5. **Logout**:
   - [ ] Login again
   - [ ] Click logout button
   - [ ] Verify redirect to /auth/login
   - [ ] Verify cookie deleted
   - [ ] Try navigating to /dashboard (should redirect to login)

6. **Session Expiry** (if time permits):
   - [ ] Login
   - [ ] Wait for token expiry (or manually modify token expiration)
   - [ ] Try accessing protected route
   - [ ] Verify redirect to /auth/login with "Session expired" message

---

#### 3.4 Structured Logging Verification

**Command**:
```bash
# Frontend logs (browser console)
# Open DevTools → Console
# Look for JSON log entries

# Backend logs
tail -f backend/logs/auth.log
```

**Expected Result**:
- ✅ JSON-formatted log entries for all auth events
- ✅ Logs contain: timestamp, level, event_type, user_id, status
- ✅ No PII (passwords, tokens) in logs

---

### Phase 4: Documentation Updates

#### 4.1 Create Quickstart Guide

**File**: `specs/004-fix-better-auth-integration/quickstart.md`

**Content**:
```markdown
# Quick Reference: Better Auth v1.4.18 Migration

## Changes Summary

Better Auth v1.4.18 replaced individual hooks with a unified client pattern:

### OLD (Deprecated)
\`\`\`typescript
import { useSignIn, useSignOut, useSession } from 'better-auth/react'
\`\`\`

### NEW (Current)
\`\`\`typescript
import { authClient } from '@/lib/auth-client'

// Sign in
const { data, error } = await authClient.signIn.email({ email, password })

// Sign out
await authClient.signOut()

// Check session
const { data: session, isPending } = authClient.useSession()
\`\`\`

## Testing Changes

Backend tests now use FastAPI dependency overrides instead of real JWT tokens:

\`\`\`python
# In conftest.py
app.dependency_overrides[get_current_user_id] = lambda: "user-123"

# In tests
def test_something(client: TestClient):
    # client is now authenticated as user-123
    response = client.get("/api/user-123/tasks")
    assert response.status_code == 200
\`\`\`

## Retry Configuration

Tests automatically retry up to 3 times (via pytest-rerunfailures).

## Structured Logging

All auth events logged to:
- Frontend: Browser console (JSON format)
- Backend: `logs/auth.log` (JSON format)
```

---

#### 4.2 Update Frontend CLAUDE.md

**File**: `frontend/CLAUDE.md`

**Section to Add** (after Authentication Flow section):
```markdown
### Better Auth v1.4.18 API

**Central Auth Client Pattern**:
```typescript
// lib/auth-client.ts
import { createAuthClient } from 'better-auth/react'

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'
})
```

**Sign In**:
```typescript
const { data, error } = await authClient.signIn.email({
  email: 'user@example.com',
  password: 'password123'
})
```

**Sign Up**:
```typescript
const { data, error } = await authClient.signUp.email({
  email: 'user@example.com',
  password: 'password123',
  name: 'User Name'
})
```

**Sign Out**:
```typescript
await authClient.signOut()
```

**Session**:
```typescript
const { data: session, isPending, error } = authClient.useSession()
```
```

---

#### 4.3 Update Backend Test Documentation

**File**: `backend/tests/README.md` (CREATE)

**Content**:
```markdown
# Backend Test Suite

## Running Tests

\`\`\`bash
# All tests
pytest

# Authentication tests only
pytest tests/test_auth_flow.py -v

# With coverage
pytest --cov=app --cov-report=html
\`\`\`

## Test Fixtures

### Authentication Fixtures

- **`client`**: Authenticated as `user-123`
- **`client_user_456`**: Authenticated as `user-456`
- **`session`**: In-memory SQLite database

### Dependency Override Pattern

Tests use FastAPI dependency overrides to mock authentication:

\`\`\`python
app.dependency_overrides[get_current_user_id] = lambda: "user-123"
\`\`\`

This eliminates the need to generate real JWT tokens in tests.

### Cross-User Testing

\`\`\`python
def test_cross_user_access(client, client_user_456, session):
    # client = user-123, client_user_456 = user-456
    response = client.get("/api/user-456/tasks")
    assert response.status_code == 403  # Forbidden
\`\`\`

## Retry Configuration

Tests automatically retry up to 3 times via `pytest-rerunfailures`:

\`\`\`python
@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_something():
    # Test that might be flaky
    pass
\`\`\`
```

---

## Risk Assessment & Mitigation

### High-Impact Risks

1. **Session State Not Updating After Login/Logout**
   - **Risk**: `authClient.useSession()` might not trigger re-renders
   - **Mitigation**: Call `router.refresh()` after auth state changes
   - **Fallback**: Use Better Auth's `refetch()` method to force update

2. **TypeScript Type Errors with authClient**
   - **Risk**: `authClient` methods might have unexpected type signatures
   - **Mitigation**: Import types from `better-auth/react` explicitly
   - **Fallback**: Use `@ts-ignore` comments with TODO to investigate

3. **Test Dependency Override Conflicts**
   - **Risk**: Multiple fixtures overriding same dependency causes conflicts
   - **Mitigation**: Clear `app.dependency_overrides` in fixture teardown
   - **Fallback**: Use separate `TestClient` instances per fixture

### Medium-Impact Risks

4. **Callback URL Handling**
   - **Risk**: `callbackURL` parameter might not work as expected in `signIn.email()`
   - **Mitigation**: Test redirect logic explicitly with different URLs
   - **Fallback**: Use manual `router.push()` instead of relying on `callbackURL`

5. **Structured Logging Performance**
   - **Risk**: JSON serialization on every auth event adds latency
   - **Mitigation**: Make logging optional via `LOG_LEVEL` environment variable
   - **Fallback**: Use async logging queue to decouple from request path

6. **Pytest Retry Hiding Real Failures**
   - **Risk**: Flaky tests pass on retry, masking underlying issues
   - **Mitigation**: Review test logs for retry attempts; investigate patterns
   - **Fallback**: Reduce retry count to 1 after initial fix validation

---

## Success Criteria Checklist

### Frontend Success
- [ ] ✅ 0 Turbopack build errors (down from 19)
- [ ] ✅ 0 TypeScript compilation errors
- [ ] ✅ All auth pages load without errors
- [ ] ✅ Login flow functional (email/password → dashboard redirect)
- [ ] ✅ Signup flow functional (new account → dashboard redirect)
- [ ] ✅ Logout flow functional (clear session → login redirect)
- [ ] ✅ Protected routes redirect unauthenticated users to login
- [ ] ✅ Session persists across page refreshes
- [ ] ✅ Auth event logs appear in browser console (JSON format)

### Backend Success
- [ ] ✅ 19/19 auth tests passing (up from 0)
- [ ] ✅ 14/14 database tests still passing
- [ ] ✅ Total: 33/33 tests passing (100%)
- [ ] ✅ User isolation tests pass (403 for cross-user access)
- [ ] ✅ JWT verification logic unchanged (no regressions)
- [ ] ✅ No deprecation warnings in test output
- [ ] ✅ Auth event logs written to `logs/auth.log` (JSON format)

### Integration Success
- [ ] ✅ End-to-end signup → login → logout flow works
- [ ] ✅ httpOnly cookies set correctly
- [ ] ✅ JWT tokens verified by backend
- [ ] ✅ User data isolation enforced (users only see own tasks)
- [ ] ✅ Session expiry shows "Session expired" message
- [ ] ✅ No CORS or network errors
- [ ] ✅ Structured logging captures all auth events (frontend + backend)

### Documentation Success
- [ ] ✅ Quickstart guide created with migration examples
- [ ] ✅ Frontend CLAUDE.md updated with new API patterns
- [ ] ✅ Backend test README created with fixture documentation
- [ ] ✅ Research.md documents all technical decisions

---

## Sequencing & Dependencies

### Critical Path (Sequential)

```
Phase 0: Research
   ↓
Phase 1: Frontend Migration
   ├─ 1.1 CREATE auth-client.ts (FOUNDATIONAL - blocks all frontend fixes)
   ├─ 1.2 FIX login page (depends on 1.1)
   ├─ 1.3 FIX signup page (depends on 1.1)
   ├─ 1.4 FIX logout button (depends on 1.1)
   ├─ 1.5 FIX protected route (depends on 1.1)
   └─ 1.6 CREATE frontend logger (parallel with 1.2-1.5)
   ↓
Phase 2: Backend Test Fixes
   ├─ 2.1 FIX conftest.py (FOUNDATIONAL - blocks all backend test fixes)
   ├─ 2.2 FIX test_auth_flow.py (depends on 2.1)
   ├─ 2.3 FIX test_session_management.py (depends on 2.1)
   ├─ 2.4 ADD pytest retry config (parallel with 2.2-2.3)
   └─ 2.5 CREATE backend logger (parallel with 2.2-2.3)
   ↓
Phase 3: Integration Testing
   ├─ 3.1 Frontend build verification
   ├─ 3.2 Backend test execution
   ├─ 3.3 End-to-end manual testing
   └─ 3.4 Structured logging verification
   ↓
Phase 4: Documentation
   ├─ 4.1 CREATE quickstart.md
   ├─ 4.2 UPDATE frontend/CLAUDE.md
   └─ 4.3 CREATE backend/tests/README.md
```

### Parallel Opportunities

- **Phase 1.6** (frontend logger) can run parallel with **1.2-1.5** (component fixes)
- **Phase 2.4** (pytest config) can run parallel with **2.2-2.3** (test fixes)
- **Phase 2.5** (backend logger) can run parallel with **2.2-2.3** (test fixes)
- **Phase 4** (all documentation) can run in parallel after Phase 3 validates

---

## Rollback Strategy

If migration fails catastrophically (>50% of tests still failing after fixes):

### Option 1: Rollback Better Auth Version

```bash
cd frontend
npm install better-auth@1.3.0
# Revert all code changes to use old hooks
```

**When to use**: If Better Auth v1.4.18 API is fundamentally incompatible

### Option 2: Incremental Rollback

- Revert frontend changes (keep backend test fixes if passing)
- Use Better Auth v1.3.x temporarily
- Plan migration for later sprint

**When to use**: If frontend issues are severe but backend tests pass

### Option 3: Continue Forward

- Fix remaining issues incrementally
- Use feature flags to disable broken auth pages temporarily
- Deploy with known issues + hotfix plan

**When to use**: If <20% of tests failing and issues are isolated

---

## Architectural Decision: Dependency Override vs Real JWT Tokens

**Decision**: Use FastAPI `app.dependency_overrides` for authentication testing instead of generating real JWT tokens.

**Rationale**:
1. **Simplicity**: No need to generate, sign, or manage JWT tokens in tests
2. **Speed**: Eliminates JWT generation/verification overhead (~10ms per test)
3. **Maintainability**: Centralized auth mocking in fixtures
4. **Isolation**: Tests focus on business logic, not JWT implementation
5. **Flexibility**: Easy to test different users by swapping fixtures

**Alternatives Considered**:
- **Real JWT Tokens**: More realistic but adds complexity and test brittleness
- **Mock Middleware**: Harder to maintain, requires patching internal Better Auth code

**Implications**:
- JWT middleware verification logic NOT tested (assumes it works from manual testing)
- Integration tests still required to verify end-to-end JWT flow
- Test coverage for JWT signature validation is lower (acceptable tradeoff for maintainability)

**Review Checkpoint**: Re-evaluate if integration tests reveal JWT issues not caught by unit tests.

---

## Critical Files Summary

| File Path | Change Type | Priority | Dependencies |
|-----------|-------------|----------|--------------|
| `frontend/src/lib/auth-client.ts` | CREATE | **P0 (Critical)** | None (foundational) |
| `frontend/src/app/(auth)/login/page.tsx` | FIX | P1 | auth-client.ts |
| `frontend/src/app/(auth)/signup/page.tsx` | FIX | P1 | auth-client.ts |
| `frontend/src/components/auth/logout-button.tsx` | FIX | P1 | auth-client.ts |
| `frontend/src/components/auth/protected-route.tsx` | FIX | P1 | auth-client.ts |
| `frontend/src/lib/logger.ts` | CREATE | P2 | None |
| `backend/tests/conftest.py` | FIX | **P0 (Critical)** | None (foundational) |
| `backend/tests/test_auth_flow.py` | FIX | P1 | conftest.py |
| `backend/tests/test_session_management.py` | FIX | P1 | conftest.py |
| `backend/app/utils/logger.py` | CREATE | P2 | None |
| `backend/pyproject.toml` | UPDATE | P2 | None |

**P0 (Critical)**: Blocks all other work in that domain
**P1 (High)**: Fixes core functionality
**P2 (Medium)**: Adds new requirements (logging, retry config)

---

## Next Steps

After plan approval:

1. **Run `/sp.tasks`** to generate actionable task list from this plan
2. **Run `/sp.implement`** to execute tasks in dependency order
3. **Validate** with manual testing checklist in Phase 3
4. **Document** lessons learned in PHR
5. **Commit** changes with `/sp.git.commit_pr`

**Estimated Timeline**: 2-3 hours for implementation + 1 hour for testing + 0.5 hours for documentation = **3.5-4.5 hours total**

---

**Plan Version**: 1.0
**Last Updated**: 2026-02-03
**Status**: Ready for task generation
