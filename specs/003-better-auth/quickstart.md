# Quickstart: Better Auth Integration Implementation Guide

**Feature**: 003-better-auth
**Date**: 2026-02-03
**Audience**: Developers implementing the authentication system

## Overview

This guide walks through implementing the complete authentication system with Better Auth, JWT tokens, httpOnly cookies, and FastAPI backend integration. Follow these steps in order.

## Prerequisites

- Frontend: Next.js 16+ installed (`frontend/` directory)
- Backend: FastAPI with Python 3.11+ (`backend/` directory)
- Database: PostgreSQL (Neon serverless) running and accessible
- Environment: Node.js 18+, Python 3.11+

## Phase 1: Frontend Better Auth Setup (30 minutes)

### Step 1.1: Install Dependencies

```bash
cd frontend
npm install better-auth @better-auth/jwt jose
```

**Packages**:
- `better-auth`: Core authentication library
- `@better-auth/jwt`: JWT plugin for token-based auth
- `jose`: JWT encoding/decoding utilities

### Step 1.2: Configure Environment Variables

Create or update `frontend/.env.local`:

```bash
# Database connection (same as backend)
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db

# Shared JWT secret (MUST match backend/.env)
BETTER_AUTH_SECRET=<generate-with-openssl-rand-hex-32>

# Backend API URL
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

**Generate secure secret**:
```bash
openssl rand -hex 32
# Example output: 7f9c8e3a2b1d4f6e8c9a0b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f
```

### Step 1.3: Create Better Auth Configuration

Create `frontend/src/lib/auth.ts`:

```typescript
import { betterAuth } from "better-auth";
import { jwtAuth } from "@better-auth/jwt";

export const auth = betterAuth({
  database: {
    url: process.env.DATABASE_URL!,
    type: "postgres"
  },
  plugins: [
    jwtAuth({
      issuer: "better-auth",
      audience: "fastapi-backend",
      expiresIn: "7d", // 7-day token expiration
      secret: process.env.BETTER_AUTH_SECRET!,
    })
  ],
  session: {
    cookieName: "better-auth.session_token",
    expiresIn: 60 * 60 * 24 * 7, // 7 days in seconds
    updateAge: 60 * 60 * 24, // Update session every 24 hours
  },
  cookie: {
    httpOnly: true, // Prevents JavaScript access (XSS protection)
    secure: process.env.NODE_ENV === "production", // HTTPS only in production
    sameSite: "lax", // CSRF protection
    path: "/",
  }
});
```

### Step 1.4: Create Better Auth API Route Handler

Create `frontend/src/app/api/auth/[...all]/route.ts`:

```typescript
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth.handler);
```

This creates all Better Auth endpoints:
- `POST /api/auth/signup`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/session`

### Step 1.5: Run Database Migrations

```bash
cd frontend
npx better-auth migrate
```

This creates the required database tables:
- `user` (core user accounts)
- `session` (active sessions)
- `account` (password hashes)
- `verification` (email verification - not used)

**Verify tables created**:
```bash
# Connect to PostgreSQL
psql $DATABASE_URL

# List tables
\dt

# Should show: user, session, account, verification
```

### Step 1.6: Update Tasks Table to Reference Users

```sql
-- Run this SQL in your database to link tasks to users
ALTER TABLE tasks
  ALTER COLUMN user_id TYPE VARCHAR(255);

ALTER TABLE tasks
  ADD CONSTRAINT fk_tasks_user
  FOREIGN KEY (user_id)
  REFERENCES "user"(id)
  ON DELETE CASCADE;
```

## Phase 2: Frontend UI Components (45 minutes)

### Step 2.1: Create Signup Page

Create `frontend/src/app/(auth)/signup/page.tsx`:

```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError('');

    const response = await fetch('/api/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
      router.push('/tasks'); // Redirect to dashboard
    } else {
      const data = await response.json();
      setError(data.message || 'Signup failed');
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={handleSubmit} className="w-full max-w-md space-y-4 p-8 bg-white rounded-lg shadow">
        <h1 className="text-2xl font-bold">Sign Up</h1>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded">{error}</div>
        )}

        <div>
          <label className="block text-sm font-medium mb-1">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            className="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500"
          />
          <p className="text-xs text-gray-500 mt-1">Minimum 8 characters</p>
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Sign Up
        </button>

        <p className="text-center text-sm">
          Already have an account?{' '}
          <a href="/login" className="text-blue-600 hover:underline">
            Log in
          </a>
        </p>
      </form>
    </div>
  );
}
```

### Step 2.2: Create Login Page

Create `frontend/src/app/(auth)/login/page.tsx`:

```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError('');

    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
      credentials: 'include', // Important: include cookies
    });

    if (response.ok) {
      router.push('/tasks'); // Redirect to dashboard
    } else {
      const data = await response.json();
      setError(data.message || 'Login failed');
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={handleSubmit} className="w-full max-w-md space-y-4 p-8 bg-white rounded-lg shadow">
        <h1 className="text-2xl font-bold">Log In</h1>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded">{error}</div>
        )}

        <div>
          <label className="block text-sm font-medium mb-1">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Log In
        </button>

        <p className="text-center text-sm">
          Don't have an account?{' '}
          <a href="/signup" className="text-blue-600 hover:underline">
            Sign up
          </a>
        </p>
      </form>
    </div>
  );
}
```

### Step 2.3: Create Logout Button Component

Create `frontend/src/components/auth/logout-button.tsx`:

```typescript
'use client';

import { useRouter } from 'next/navigation';

export function LogoutButton() {
  const router = useRouter();

  async function handleLogout() {
    const response = await fetch('/api/auth/logout', {
      method: 'POST',
      credentials: 'include',
    });

    if (response.ok) {
      router.push('/login');
    }
  }

  return (
    <button
      onClick={handleLogout}
      className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded hover:bg-red-700"
    >
      Log Out
    </button>
  );
}
```

## Phase 3: Frontend API Proxy (30 minutes)

### Step 3.1: Create API Proxy Route

Create `frontend/src/app/api/proxy/[...path]/route.ts`:

```typescript
import { cookies } from 'next/headers';
import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'edge'; // Use Edge runtime for better performance

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export async function GET(request: NextRequest, { params }: { params: { path: string[] } }) {
  return handleRequest(request, params.path, 'GET');
}

export async function POST(request: NextRequest, { params }: { params: { path: string[] } }) {
  return handleRequest(request, params.path, 'POST');
}

export async function PUT(request: NextRequest, { params }: { params: { path: string[] } }) {
  return handleRequest(request, params.path, 'PUT');
}

export async function DELETE(request: NextRequest, { params }: { params: { path: string[] } }) {
  return handleRequest(request, params.path, 'DELETE');
}

export async function PATCH(request: NextRequest, { params }: { params: { path: string[] } }) {
  return handleRequest(request, params.path, 'PATCH');
}

async function handleRequest(request: NextRequest, pathSegments: string[], method: string) {
  try {
    // Read JWT token from httpOnly cookie (server-side only)
    const cookieStore = cookies();
    const sessionToken = cookieStore.get('better-auth.session_token')?.value;

    if (!sessionToken) {
      return NextResponse.json(
        { error: 'Unauthorized', message: 'No session token found' },
        { status: 401 }
      );
    }

    // Construct backend URL
    const path = pathSegments.join('/');
    const backendUrl = `${BACKEND_URL}/api/${path}`;

    // Forward request to backend with Authorization header
    const headers = new Headers();
    headers.set('Authorization', `Bearer ${sessionToken}`);
    headers.set('Content-Type', 'application/json');

    const requestOptions: RequestInit = {
      method,
      headers,
    };

    // Include body for POST, PUT, PATCH
    if (['POST', 'PUT', 'PATCH'].includes(method)) {
      const body = await request.json();
      requestOptions.body = JSON.stringify(body);
    }

    // Make request to backend
    const response = await fetch(backendUrl, requestOptions);
    const data = await response.json();

    // Forward response from backend
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json(
      { error: 'Internal Server Error', message: 'Failed to proxy request' },
      { status: 500 }
    );
  }
}
```

### Step 3.2: Create API Client Helper

Create `frontend/src/lib/api-client.ts`:

```typescript
export async function apiCall(url: string, options?: RequestInit) {
  const response = await fetch(url, {
    ...options,
    credentials: 'include', // Always include cookies
  });

  // Handle expired token
  if (response.status === 401) {
    window.location.href = '/login?message=Session expired. Please log in again.';
    throw new Error('Session expired');
  }

  // Handle forbidden (user_id mismatch)
  if (response.status === 403) {
    throw new Error('Access denied');
  }

  return response;
}

// Task API methods
export async function fetchTasks(userId: string) {
  const response = await apiCall(`/api/proxy/${userId}/tasks`);
  return response.json();
}

export async function createTask(userId: string, task: { title: string; description?: string }) {
  const response = await apiCall(`/api/proxy/${userId}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(task),
  });
  return response.json();
}

export async function updateTask(userId: string, taskId: number, updates: Partial<{ title: string; description: string; completed: boolean }>) {
  const response = await apiCall(`/api/proxy/${userId}/tasks/${taskId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates),
  });
  return response.json();
}

export async function deleteTask(userId: string, taskId: number) {
  const response = await apiCall(`/api/proxy/${userId}/tasks/${taskId}`, {
    method: 'DELETE',
  });
  return response.json();
}
```

## Phase 4: Backend JWT Verification (45 minutes)

### Step 4.1: Install Dependencies

```bash
cd backend
uv add pyjwt python-multipart
```

**Packages**:
- `pyjwt`: JWT encoding/decoding (recommended, actively maintained)
- `python-multipart`: Form data parsing (required by FastAPI)

### Step 4.2: Configure Environment Variables

Create or update `backend/.env`:

```bash
# Shared JWT secret (MUST match frontend/.env.local)
BETTER_AUTH_SECRET=<same-secret-as-frontend>

# Database connection
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
```

### Step 4.3: Create JWT Auth Dependencies

Create `backend/app/dependencies/auth.py`:

```python
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os

# JWT configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"
ISSUER = "better-auth"
AUDIENCE = "fastapi-backend"

security = HTTPBearer()

async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> str:
    """
    Verify JWT token and extract user_id from 'sub' claim.

    Raises:
        HTTPException: 401 if token is invalid, expired, or missing
    """
    token = credentials.credentials

    try:
        # Decode and verify JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            issuer=ISSUER,
            audience=AUDIENCE,
        )

        # Extract user_id from 'sub' claim
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def verify_user_id_match(
    user_id: str,
    current_user_id: Annotated[str, Depends(get_current_user_id)]
) -> str:
    """
    Verify that the user_id from URL matches the authenticated user.

    Args:
        user_id: User ID from URL path parameter
        current_user_id: User ID extracted from JWT token

    Returns:
        str: The verified user_id

    Raises:
        HTTPException: 403 if user IDs don't match
    """
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch"
        )

    return user_id
```

### Step 4.4: Update Task Routes with Auth

Update `backend/app/routes/tasks.py`:

```python
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.dependencies.auth import verify_user_id_match
from app.dependencies.database import get_session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    user_id: Annotated[str, Depends(verify_user_id_match)],
    session: Annotated[Session, Depends(get_session)]
):
    """List all tasks for authenticated user."""
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: Annotated[str, Depends(verify_user_id_match)],
    task_data: TaskCreate,
    session: Annotated[Session, Depends(get_session)]
):
    """Create a new task for authenticated user."""
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: Annotated[str, Depends(verify_user_id_match)],
    task_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    """Get a specific task by ID (user isolation enforced)."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: Annotated[str, Depends(verify_user_id_match)],
    task_id: int,
    task_data: TaskCreate,
    session: Annotated[Session, Depends(get_session)]
):
    """Update a task (user isolation enforced)."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task.title = task_data.title
    task.description = task_data.description
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}")
async def delete_task(
    user_id: Annotated[str, Depends(verify_user_id_match)],
    task_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    """Delete a task (user isolation enforced)."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()
    return {"success": True, "message": "Task deleted successfully"}

@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: Annotated[str, Depends(verify_user_id_match)],
    task_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    """Toggle task completion status (user isolation enforced)."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Step 4.5: Configure CORS in Main App

Update `backend/app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import tasks

app = FastAPI(title="Todo API with Authentication")

# CORS configuration for cookie credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development frontend
        "https://yourdomain.com",  # Production frontend (update as needed)
    ],
    allow_credentials=True,  # Required for cookies
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)

# Include routers
app.include_router(tasks.router)

@app.get("/")
async def root():
    return {"message": "Todo API with Authentication"}
```

## Testing the Authentication System

### Test 1: User Signup

```bash
# Via frontend UI
Open http://localhost:3000/signup
Enter email: test@example.com
Enter password: password123 (8+ chars)
Click "Sign Up"
→ Should create account and redirect to /tasks

# Via API directly
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### Test 2: User Login

```bash
# Via frontend UI
Open http://localhost:3000/login
Enter email: test@example.com
Enter password: password123
Click "Log In"
→ Should log in and redirect to /tasks

# Via API directly
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  -c cookies.txt  # Save cookies
```

### Test 3: Authenticated API Request

```bash
# Using proxy (from browser or with cookies)
curl http://localhost:3000/api/proxy/usr_cm5x8y9z0000/tasks \
  -b cookies.txt  # Use saved cookies from login
```

### Test 4: User Data Isolation

```bash
# Create second user
curl -X POST http://localhost:3000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user2@example.com","password":"password456"}'

# Try to access first user's tasks while logged in as second user
# Should return 403 Forbidden with "Access denied: user_id mismatch"
```

### Test 5: Logout

```bash
# Via frontend UI
Click "Log Out" button
→ Should clear cookie and redirect to /login

# Via API directly
curl -X POST http://localhost:3000/api/auth/logout \
  -b cookies.txt
→ Should return success and clear cookie
```

## Troubleshooting

### Issue: "No session token found" after login

**Solution**: Check that cookies are being set properly. Inspect browser DevTools → Application → Cookies → `better-auth.session_token` should exist.

### Issue: "Invalid token" from backend

**Solution**: Verify `BETTER_AUTH_SECRET` is identical in both `frontend/.env.local` and `backend/.env`.

### Issue: CORS errors in browser

**Solution**: Ensure `allow_credentials=True` and `allow_origins` does NOT include `"*"` (wildcard not allowed with credentials).

### Issue: 403 Forbidden on API requests

**Solution**: Check that the `user_id` in the URL matches the `sub` claim in the JWT token. Example: User ID `usr_cm5x8y9z0000` must access `/api/usr_cm5x8y9z0000/tasks`.

## Next Steps

1. Implement protected route wrapper for frontend pages
2. Add session restoration on page load (read `/api/auth/session`)
3. Create "redirect after login" functionality (save intended route before login)
4. Add error handling for network failures during auth
5. Implement session expiration UI messaging

---

**Quickstart Complete** | Authentication system ready for implementation via `/sp.tasks`
