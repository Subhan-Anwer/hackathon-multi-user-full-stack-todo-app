# Better Auth Integration with Next.js and FastAPI - Comprehensive Research

**Research Date:** 2026-02-03
**Purpose:** Document architecture, patterns, and best practices for integrating Better Auth with Next.js 16 frontend and FastAPI backend

---

## Table of Contents

1. [Better Auth Library Architecture](#1-better-auth-library-architecture)
2. [Next.js API Proxy Pattern](#2-nextjs-api-proxy-pattern)
3. [FastAPI JWT Verification](#3-fastapi-jwt-verification)
4. [Security Best Practices](#4-security-best-practices)
5. [Database Schema for Users](#5-database-schema-for-users)
6. [Complete Authentication Flow](#6-complete-authentication-flow)
7. [Implementation Decisions](#7-implementation-decisions)

---

## 1. Better Auth Library Architecture

### 1.1 JWT Token Generation

Better Auth **primarily uses session-based authentication** with httpOnly cookies by default, **not JWT tokens**. However, it provides a **JWT plugin** for generating JWT tokens when needed for API authentication.

#### JWT Plugin Configuration

```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    jwt({
      jwt: {
        issuer: "https://example.com",
        audience: "https://example.com",
        expirationTime: "1h", // Token expiration
        getSubject: (session) => {
          // By default the subject is the user id
          // Can be customized to use email or other identifier
          return session.user.id; // or session.user.email
        }
      }
    })
  ]
});
```

**Key Points:**
- JWT plugin is **optional** and must be explicitly added
- Default `sub` (subject) claim is the user ID
- Can customize `iss` (issuer), `aud` (audience), `exp` (expiration)
- Token expiration configurable (e.g., "1h", "15m", "7d")

#### JWT Payload Structure

Standard JWT payload from Better Auth includes:

```json
{
  "sub": "user-id-here",           // Subject (user identifier)
  "iss": "https://example.com",    // Issuer
  "aud": "https://example.com",    // Audience
  "exp": 1234567890,               // Expiration timestamp
  "iat": 1234567890,               // Issued at timestamp
  "jti": "unique-token-id"         // JWT ID (optional)
}
```

#### Retrieving JWT from Session

```typescript
// Client-side: Get JWT from response header
await authClient.getSession({
  fetchOptions: {
    onSuccess: (ctx) => {
      const jwt = ctx.response.headers.get("set-auth-jwt");
      // Use this JWT for backend API calls
    }
  }
});
```

### 1.2 httpOnly Cookie Configuration

Better Auth uses **httpOnly cookies** as the primary authentication mechanism for web applications.

#### Default Cookie Settings

```typescript
export const auth = betterAuth({
  advanced: {
    // Force cookies to always be secure (production default)
    useSecureCookies: true,

    // Default cookie attributes applied to all cookies
    defaultCookieAttributes: {
      httpOnly: true,  // Prevents JavaScript access
      secure: true,    // HTTPS only (auto-enabled in production)
      sameSite: "lax"  // CSRF protection (default)
    },

    // Custom cookie configuration for specific cookies
    cookies: {
      session_token: {
        name: "session_token", // Default name
        attributes: {
          httpOnly: true,
          secure: true,
          sameSite: "lax"
        }
      }
    },

    // Custom cookie prefix for all auth cookies
    cookiePrefix: "myapp"
  }
});
```

#### Cookie Names Used by Better Auth

| Cookie Name | Purpose | Default Value |
|------------|---------|---------------|
| `session_token` | Session token | Required for authentication |
| `session_data` | Cached session data | Optional performance optimization |
| `dont_remember` | Remember me flag | Indicates session persistence |
| `two_factor` | 2FA state | Plugin-specific (if enabled) |

**Security Attributes:**
- **httpOnly**: `true` (blocks client-side JavaScript access)
- **secure**: `true` in production (HTTPS only)
- **sameSite**: `"lax"` by default (CSRF protection)
- All cookies are **signed** using `BETTER_AUTH_SECRET`

#### Cross-Domain Cookie Configuration

For cross-domain scenarios (e.g., frontend on `app.example.com`, backend on `api.example.com`):

```typescript
export const auth = betterAuth({
  advanced: {
    // Cross-subdomain cookies
    crossSubDomainCookies: {
      enabled: true,
      additionalCookies: ["custom_cookie"],
      domain: "example.com" // Root domain
    },

    // OR for completely different domains
    defaultCookieAttributes: {
      sameSite: "none",    // Required for cross-domain
      secure: true,        // Required with sameSite=none
      partitioned: true    // New browser standard for 3rd-party cookies
    }
  }
});
```

**Important:** When `sameSite: "none"`, **HTTPS is mandatory** (`secure: true`).

### 1.3 Session Management Patterns

Better Auth supports **two session management strategies**:

#### Strategy 1: Database Session (Default)

```typescript
export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL
  }),
  // Sessions stored in database
  // Cookie contains only session token (reference)
});
```

**Flow:**
1. Client sends cookie with `session_token`
2. Server queries database for session details
3. Returns user data if session valid

**Pros:** Most secure, supports session revocation
**Cons:** Database query on every request

#### Strategy 2: Stateless Session (Cookie Cache)

```typescript
export const auth = betterAuth({
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 7 * 24 * 60 * 60, // 7 days
      strategy: "jwe",  // or "jwt" or "compact"
      refreshCache: true // Auto-refresh on access
    }
  },
  account: {
    storeStateStrategy: "cookie",
    storeAccountCookie: true // Store account data in cookie
  }
});
```

**Encryption Strategies:**
- **`jwe`**: JSON Web Encryption (most secure, encrypted)
- **`jwt`**: JSON Web Token (signed, not encrypted)
- **`compact`**: Compact representation (smallest size)

**Flow:**
1. Client sends cookie with encrypted session data
2. Server decrypts cookie locally (no DB query)
3. Returns user data if valid

**Pros:** No database queries, faster
**Cons:** Sessions cannot be revoked without waiting for expiration

**Recommendation:** Use **database sessions** for this project to support user management and session revocation.

---

## 2. Next.js API Proxy Pattern

### 2.1 Server-Side Cookie Reading in Next.js App Router

Next.js 16 App Router provides `cookies()` function from `next/headers` for server-side cookie access.

#### Reading Cookies in Server Components

```typescript
import { cookies } from 'next/headers';

export default async function Page() {
  const cookieStore = await cookies();
  const sessionToken = cookieStore.get('session_token');

  // Use session token for authentication
  return <div>User authenticated</div>;
}
```

#### Reading Cookies in Route Handlers (API Routes)

```typescript
import { cookies } from 'next/headers';
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const cookieStore = await cookies();
  const sessionToken = cookieStore.get('session_token');

  return NextResponse.json({ sessionToken });
}
```

**Key Points:**
- `cookies()` must be **awaited** in Next.js 15+
- Returns **read-only** cookie store in Server Components
- Can **read, set, delete** cookies in Route Handlers

### 2.2 API Proxy Pattern for Cookie-to-Header Forwarding

The recommended pattern for forwarding cookies as Authorization headers to the backend API:

#### Pattern 1: Edge API Route Proxy

```typescript
// app/api/proxy/[...path]/route.ts
import { type NextRequest } from 'next/server';

export const config = {
  runtime: 'edge', // Optimal performance
};

export default async function handler(req: NextRequest) {
  // Extract session token from httpOnly cookie
  const sessionToken = req.cookies.get('session_token')?.value;

  // Get the path after /api/proxy/
  const path = req.nextUrl.pathname.replace('/api/proxy/', '');

  // Forward to backend with Authorization header
  return fetch(`${process.env.BACKEND_URL}/${path}`, {
    method: req.method,
    headers: {
      'Authorization': `Bearer ${sessionToken}`,
      'Content-Type': 'application/json',
    },
    body: req.method !== 'GET' && req.method !== 'HEAD'
      ? await req.text()
      : undefined,
    redirect: 'manual',
  });
}
```

**Why Edge Runtime?**
- Faster cold starts
- Lower latency
- Better for simple proxy logic
- No Node.js API dependencies needed

#### Pattern 2: Node.js API Route Proxy (Full Control)

```typescript
// app/api/tasks/[...path]/route.ts
import { cookies } from 'next/headers';
import { NextRequest, NextResponse } from 'next/server';

async function proxyToBackend(
  req: NextRequest,
  path: string
): Promise<NextResponse> {
  const cookieStore = await cookies();
  const sessionToken = cookieStore.get('session_token')?.value;

  if (!sessionToken) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  const backendUrl = `${process.env.BACKEND_URL}${path}`;

  try {
    const response = await fetch(backendUrl, {
      method: req.method,
      headers: {
        'Authorization': `Bearer ${sessionToken}`,
        'Content-Type': 'application/json',
      },
      body: ['GET', 'HEAD'].includes(req.method || '')
        ? undefined
        : await req.text(),
    });

    const data = await response.json();

    return NextResponse.json(data, {
      status: response.status
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Backend request failed' },
      { status: 500 }
    );
  }
}

export async function GET(req: NextRequest) {
  return proxyToBackend(req, req.nextUrl.pathname);
}

export async function POST(req: NextRequest) {
  return proxyToBackend(req, req.nextUrl.pathname);
}

export async function PUT(req: NextRequest) {
  return proxyToBackend(req, req.nextUrl.pathname);
}

export async function DELETE(req: NextRequest) {
  return proxyToBackend(req, req.nextUrl.pathname);
}

export async function PATCH(req: NextRequest) {
  return proxyToBackend(req, req.nextUrl.pathname);
}
```

### 2.3 Handling All HTTP Methods

**HTTP Methods to Support:**
- **GET**: Retrieve resources
- **POST**: Create resources
- **PUT**: Update/replace resources
- **PATCH**: Partial update resources
- **DELETE**: Delete resources
- **OPTIONS**: CORS preflight (handled by middleware)

**Best Practice:** Create a **generic proxy function** that handles all methods (shown in Pattern 2 above).

### 2.4 Error Handling and Response Forwarding

```typescript
async function proxyWithErrorHandling(
  req: NextRequest,
  path: string
): Promise<NextResponse> {
  try {
    const cookieStore = await cookies();
    const sessionToken = cookieStore.get('session_token')?.value;

    if (!sessionToken) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      );
    }

    const response = await fetch(`${process.env.BACKEND_URL}${path}`, {
      method: req.method,
      headers: {
        'Authorization': `Bearer ${sessionToken}`,
        'Content-Type': 'application/json',
      },
      body: req.method !== 'GET' ? await req.text() : undefined,
    });

    // Forward backend response as-is
    const data = await response.text();

    return new NextResponse(data, {
      status: response.status,
      headers: {
        'Content-Type': response.headers.get('Content-Type') || 'application/json',
      },
    });
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

**Error Response Codes:**
- **401 Unauthorized**: Missing or invalid session token
- **403 Forbidden**: Valid token but insufficient permissions
- **500 Internal Server Error**: Backend communication failure
- **502 Bad Gateway**: Backend unreachable
- **504 Gateway Timeout**: Backend timeout

---

## 3. FastAPI JWT Verification

### 3.1 PyJWT vs python-jose Comparison

**DECISION: Use PyJWT** ✅

| Feature | PyJWT | python-jose |
|---------|-------|-------------|
| **Maintenance** | ✅ Active (2024+) | ❌ Abandoned (last update 2021) |
| **Python 3.11+ Support** | ✅ Full support | ❌ Deprecated on Python 3.10+ |
| **Security Updates** | ✅ Regular | ❌ No recent updates |
| **Size** | ✅ Lightweight | ❌ Heavier dependencies |
| **FastAPI Docs** | ✅ Now recommended | ⚠️ Old examples still reference it |
| **Features** | JWT only | JWT + JWE + JWS |

**Why PyJWT?**
- **Actively maintained** with regular security patches
- **Officially recommended** by FastAPI (as of 2024)
- **Simpler API** focused on JWT operations
- **Better compatibility** with Python 3.11+
- **Smaller footprint** with fewer dependencies

**Installation:**
```bash
pip install pyjwt
```

### 3.2 Middleware vs Dependency Injection

**DECISION: Use Dependency Injection** ✅

#### Comparison

| Approach | Pros | Cons | Use Case |
|----------|------|------|----------|
| **Dependency Injection** | - Granular control<br>- Can exclude specific endpoints<br>- Better testability<br>- Clear dependencies | - Must add to each route | Most API endpoints |
| **Middleware** | - Global application<br>- DRY principle<br>- Runs on all requests | - Harder to exclude routes<br>- Less flexible | Rate limiting, logging |

#### Recommended Approach: Dependency Injection

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Annotated

# Security scheme
security = HTTPBearer()

# JWT Configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

# Dependency to verify JWT and extract user
async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> dict:
    """
    Verify JWT token and extract user information.

    Raises:
        HTTPException: 401 if token is invalid or expired
    """
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode and verify JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Extract user ID from 'sub' claim
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        return {"user_id": user_id, "payload": payload}

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

# Use in routes
@app.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    # Verify user_id matches token
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user_id mismatch"
        )

    # Return user's tasks
    return {"tasks": [...]}
```

### 3.3 Extracting user_id from JWT Payload

The **`sub` (subject) field** is the **standard JWT claim** for user identification.

#### Standard JWT Claims

| Claim | Name | Purpose | Example |
|-------|------|---------|---------|
| `sub` | Subject | **User identifier** | `"user-123"` |
| `iss` | Issuer | Token issuer | `"https://auth.example.com"` |
| `aud` | Audience | Intended recipient | `"https://api.example.com"` |
| `exp` | Expiration | Expiration timestamp | `1234567890` |
| `iat` | Issued At | Issue timestamp | `1234567800` |
| `jti` | JWT ID | Unique token ID | `"abc-123"` |

#### Extracting user_id

```python
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

def extract_user_id(token: str, secret: str) -> str:
    """Extract user ID from JWT token."""
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        user_id = payload.get("sub")

        if not user_id:
            raise ValueError("Missing 'sub' claim in token")

        return user_id

    except ExpiredSignatureError:
        raise ValueError("Token has expired")
    except InvalidTokenError:
        raise ValueError("Invalid token")
```

#### Complete Verification with Error Handling

```python
import jwt
from fastapi import HTTPException, status

async def verify_and_extract_user(token: str) -> dict:
    """
    Verify JWT and extract all relevant user information.

    Returns:
        dict with user_id and other claims
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"],
            # Optional: verify additional claims
            audience="https://api.example.com",
            issuer="https://auth.example.com",
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iat": True,
                "require": ["sub", "exp", "iat"]  # Required claims
            }
        )

        return {
            "user_id": payload["sub"],
            "email": payload.get("email"),
            "exp": payload["exp"],
            "iat": payload["iat"]
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidAudienceError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token audience"
        )
    except jwt.InvalidIssuerError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token issuer"
        )
    except jwt.MissingRequiredClaimError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Missing required claim: {e.claim}"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

### 3.4 Error Responses: 401 vs 403

**HTTP Status Code Standards:**

| Status Code | Name | When to Use | Scenario |
|------------|------|-------------|----------|
| **401 Unauthorized** | Authentication Required | Missing, invalid, or expired token | User not logged in |
| **403 Forbidden** | Access Denied | Valid token but insufficient permissions | User logged in but lacks access |

#### 401 Unauthorized

Use when:
- No `Authorization` header provided
- Invalid JWT signature
- Expired JWT token
- Malformed JWT token
- Missing required claims

```python
# Missing or invalid token
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}  # MUST include for 401
)
```

**Important:** 401 responses **MUST** include `WWW-Authenticate` header per RFC 7235.

#### 403 Forbidden

Use when:
- Valid token provided
- User authenticated successfully
- But user lacks permission for the resource

```python
# Valid user but trying to access another user's data
if current_user["user_id"] != requested_user_id:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access forbidden: insufficient permissions"
    )
```

#### Complete Example

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Annotated

security = HTTPBearer()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> dict:
    """Extract and validate user from JWT token."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return {"user_id": user_id}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

@app.get("/api/{user_id}/tasks")
async def get_user_tasks(
    user_id: str,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    # User is authenticated (passed get_current_user)
    # But check if they can access this user_id
    if current_user["user_id"] != user_id:
        # 403: Valid user but wrong resource
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's tasks"
        )

    # User can access their own tasks
    return {"tasks": [...]}
```

---

## 4. Security Best Practices

### 4.1 CORS Configuration for Cookie Credentials

CORS (Cross-Origin Resource Sharing) must be properly configured when frontend and backend are on different origins.

#### FastAPI CORS Configuration

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration for cookie-based authentication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Development
        "https://app.example.com",    # Production
    ],
    allow_credentials=True,  # REQUIRED for cookies
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    expose_headers=["Content-Length", "X-Total-Count"],
    max_age=600,  # Cache preflight response for 10 minutes
)
```

**Critical Settings for Cookies:**

1. **`allow_credentials=True`**
   - **MUST** be set to allow cookies
   - Frontend must send `credentials: 'include'` in fetch requests

2. **`allow_origins`**
   - **CANNOT** use `["*"]` when `allow_credentials=True`
   - Must specify **exact origins**

3. **`allow_methods`**
   - List all HTTP methods your API supports
   - Can use `["*"]` for all methods (but explicit is better)

4. **`allow_headers`**
   - Must include `"Authorization"` for Bearer tokens
   - `"Content-Type"` for JSON requests

#### Better Auth Express CORS Example

```typescript
import cors from "cors";

app.use(
  cors({
    origin: "http://localhost:3000",
    methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    credentials: true,  // Allow cookies
    allowedHeaders: ["Content-Type", "Authorization"],
  })
);
```

#### Frontend Fetch Configuration

```typescript
// Client-side fetch must include credentials
fetch('http://localhost:8000/api/tasks', {
  method: 'GET',
  credentials: 'include',  // Send cookies
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### 4.2 Cookie Attributes (httpOnly, secure, sameSite)

#### Cookie Attribute Reference

| Attribute | Values | Purpose | Recommendation |
|-----------|--------|---------|----------------|
| **httpOnly** | `true`/`false` | Blocks JavaScript access | ✅ **Always `true`** |
| **secure** | `true`/`false` | HTTPS only | ✅ **`true` in production** |
| **sameSite** | `strict`/`lax`/`none` | CSRF protection | ✅ **`lax`** (or `none` for cross-domain) |
| **domain** | `.example.com` | Cookie scope | Set for subdomain sharing |
| **path** | `/` | URL path scope | Usually `/` |
| **maxAge** | Seconds | Cookie lifetime | Session or long-lived |

#### Security Configuration

```typescript
// Better Auth configuration
export const auth = betterAuth({
  advanced: {
    defaultCookieAttributes: {
      httpOnly: true,    // ✅ Prevent XSS attacks
      secure: true,      // ✅ HTTPS only (production)
      sameSite: "lax",   // ✅ CSRF protection
      path: "/",
      maxAge: 60 * 60 * 24 * 7  // 7 days
    }
  }
});
```

#### sameSite Values Explained

| Value | Behavior | Use Case |
|-------|----------|----------|
| **`strict`** | Never sent cross-origin | Highest security, can break OAuth flows |
| **`lax`** ✅ | Sent on top-level navigation (GET) | **Recommended default** |
| **`none`** | Always sent (requires `secure=true`) | Cross-domain auth (different origins) |

**Recommendation for This Project:**

```typescript
// Same domain (e.g., localhost:3000 -> localhost:8000)
sameSite: "lax"

// Different domains (e.g., app.example.com -> api.example.com)
sameSite: "none",
secure: true,
partitioned: true  // New browser standard
```

### 4.3 JWT Secret Management and Rotation

#### Secret Key Requirements

**Minimum Requirements:**
- **Length**: 256 bits (32 bytes) minimum for HS256
- **Randomness**: Cryptographically secure random
- **Storage**: Environment variables (never commit to git)

#### Generating Secure Secrets

```bash
# Using OpenSSL
openssl rand -hex 32

# Using Python
python -c "import secrets; print(secrets.token_hex(32))"

# Using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

#### Environment Variable Configuration

```bash
# .env (NEVER commit this file)
BETTER_AUTH_SECRET=your-256-bit-secret-here
DATABASE_URL=postgresql://user:pass@host:5432/db
```

**Frontend (.env.local):**
```bash
BETTER_AUTH_SECRET=your-256-bit-secret-here
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend (.env):**
```bash
BETTER_AUTH_SECRET=your-256-bit-secret-here
DATABASE_URL=postgresql://user:pass@host:5432/db
```

**CRITICAL:** Both frontend and backend **MUST** use the **same secret** for JWT signing/verification.

#### Secret Rotation Strategy

**Why Rotate Secrets?**
- Comply with security policies
- Mitigate leaked secret exposure
- Regular security hygiene

**Rotation Process:**

```python
# Support multiple secrets during rotation
CURRENT_SECRET = os.getenv("BETTER_AUTH_SECRET")
PREVIOUS_SECRET = os.getenv("BETTER_AUTH_SECRET_OLD")

async def verify_token_with_rotation(token: str) -> dict:
    """Try current secret first, fall back to old secret."""
    try:
        # Try current secret
        payload = jwt.decode(token, CURRENT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError:
        # Fall back to old secret during rotation period
        if PREVIOUS_SECRET:
            try:
                payload = jwt.decode(token, PREVIOUS_SECRET, algorithms=["HS256"])
                # Log that old secret was used (migration needed)
                logger.warning("Token verified with old secret")
                return payload
            except jwt.InvalidTokenError:
                pass
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

**Rotation Steps:**
1. Deploy code supporting both `CURRENT_SECRET` and `PREVIOUS_SECRET`
2. Update `CURRENT_SECRET` to new value, move old to `PREVIOUS_SECRET`
3. Wait for all old tokens to expire (max token lifetime)
4. Remove `PREVIOUS_SECRET` support

### 4.4 Token Expiration Handling

#### Setting Expiration

**Better Auth Configuration:**
```typescript
jwt({
  jwt: {
    expirationTime: "1h",  // 1 hour
    // Other options: "15m", "7d", "30d"
  }
})
```

**PyJWT Token Creation:**
```python
from datetime import datetime, timezone, timedelta
import jwt

def create_token(user_id: str) -> str:
    """Create JWT token with expiration."""
    payload = {
        "sub": user_id,
        "iat": datetime.now(tz=timezone.utc),
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

#### Handling Expired Tokens

```python
import jwt
from fastapi import HTTPException, status

async def verify_token(token: str) -> dict:
    """Verify token and handle expiration."""
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"],
            options={
                "verify_exp": True,  # Verify expiration
            }
        )
        return payload

    except jwt.ExpiredSignatureError:
        # Token expired - user needs to re-authenticate
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={
                "WWW-Authenticate": "Bearer",
                "X-Token-Expired": "true"  # Custom header for client
            }
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
```

#### Client-Side Expiration Handling

```typescript
// Frontend: Handle expired tokens
async function apiCall(endpoint: string) {
  try {
    const response = await fetch(endpoint, {
      credentials: 'include'
    });

    if (response.status === 401) {
      const tokenExpired = response.headers.get('X-Token-Expired');

      if (tokenExpired) {
        // Redirect to login
        window.location.href = '/login';
      }
    }

    return response.json();
  } catch (error) {
    console.error('API call failed:', error);
  }
}
```

#### Recommended Expiration Times

| Token Type | Lifetime | Rationale |
|------------|----------|-----------|
| **Access Token** | 15min - 1h | Short-lived for security |
| **Refresh Token** | 7d - 30d | Long-lived for UX |
| **Session Cookie** | 7d | Balance security/UX |
| **Remember Me** | 30d - 1y | Persistent login |

**For This Project:**
- **Session Cookie**: 7 days
- **JWT Access Token**: 1 hour (if using JWT plugin)

---

## 5. Database Schema for Users

### 5.1 Does Better Auth Create Users Table Automatically?

**YES** - Better Auth automatically creates required database tables using its CLI migration tool.

#### Core Tables Created

Better Auth creates **4 core tables** automatically:

1. **`user`** - User accounts
2. **`session`** - Active sessions
3. **`account`** - OAuth accounts (social login)
4. **`verification`** - Email/phone verification tokens

#### CLI Migration Commands

```bash
# Generate migration (for custom adapters like Kysely)
npx @better-auth/cli generate

# Migrate database (for built-in adapters like pg)
npx @better-auth/cli migrate
```

**Process:**
1. Configure Better Auth with database connection
2. Run migration command
3. CLI detects missing tables/columns
4. Generates SQL or applies migrations automatically

#### Schema Detection

Better Auth CLI:
- **Scans existing database** for tables
- **Compares with required schema** (from config + plugins)
- **Generates only missing tables/columns**
- **Supports PostgreSQL schemas** (respects `search_path`)

### 5.2 Required Fields (id, email, password_hash)

#### User Table Schema

```typescript
// Better Auth user table structure
interface User {
  id: string;              // Primary key (UUID or nanoid)
  email: string;           // Unique, required
  emailVerified: boolean;  // Email verification status
  name: string | null;     // Display name (optional)
  image: string | null;    // Avatar URL (optional)
  createdAt: Date;         // Registration timestamp
  updatedAt: Date;         // Last update timestamp
}
```

**Password Storage:**
Better Auth stores password hashes in a **separate `account` table** for security and flexibility.

#### Account Table Schema

```typescript
interface Account {
  id: string;              // Primary key
  userId: string;          // Foreign key to user.id
  accountId: string;       // Provider-specific ID (or email for credentials)
  providerId: string;      // "credential" | "google" | "github" | etc.
  accessToken: string | null;     // OAuth access token
  refreshToken: string | null;    // OAuth refresh token
  idToken: string | null;         // OAuth ID token
  expiresAt: Date | null;         // Token expiration
  password: string | null;        // Hashed password (credential provider only)
  createdAt: Date;
  updatedAt: Date;
}
```

**Key Points:**
- Password hash stored in `account.password` (NOT `user` table)
- Only present when `providerId = "credential"`
- Uses **Argon2id** hashing by default (most secure)

#### Session Table Schema

```typescript
interface Session {
  id: string;              // Primary key
  userId: string;          // Foreign key to user.id
  sessionToken: string;    // Unique session identifier
  expiresAt: Date;         // Session expiration
  ipAddress: string | null;       // Client IP (if tracking enabled)
  userAgent: string | null;       // Browser/device info
  createdAt: Date;
  updatedAt: Date;
}
```

#### Verification Table Schema

```typescript
interface Verification {
  id: string;              // Primary key
  identifier: string;      // Email or phone
  value: string;           // Verification code/token
  expiresAt: Date;         // Code expiration
  createdAt: Date;
  updatedAt: Date;
}
```

### 5.3 Integration with Existing PostgreSQL Schema

#### Approach 1: Let Better Auth Manage Auth Tables

**Recommended for this project** ✅

```typescript
// auth.ts
import { betterAuth } from "better-auth";
import { Pool } from "pg";

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL
  }),
  // Better Auth creates: user, session, account, verification
});
```

**Benefits:**
- No manual schema management
- Automatic migrations
- Future-proof (plugin support)

#### Approach 2: Custom Schema with Better Auth

If you need custom user fields:

```typescript
import { betterAuth } from "better-auth";
import { Pool } from "pg";

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL
  }),
  user: {
    additionalFields: {
      // Custom fields added to user table
      role: {
        type: "string",
        required: false,
        defaultValue: "user"
      },
      preferences: {
        type: "json",
        required: false
      }
    }
  }
});
```

**Schema Extension Process:**
1. Define additional fields in config
2. Run `npx @better-auth/cli migrate`
3. CLI adds columns to existing tables

#### Integration with Tasks Table

```sql
-- Tasks table references Better Auth user table
CREATE TABLE tasks (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster user task queries
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

**Foreign Key Relationship:**
- `tasks.user_id` → `user.id`
- Enforces referential integrity
- `ON DELETE CASCADE` removes tasks when user deleted

#### PostgreSQL Schema Organization

Better Auth supports **PostgreSQL schemas** (namespaces):

```typescript
// Configure schema via connection string
const pool = new Pool({
  connectionString: "postgresql://user:pass@host:5432/db?options=-c%20search_path=auth"
});

// OR via ALTER USER
// ALTER USER authuser SET search_path TO auth, public;
```

**Benefits:**
- Isolate auth tables from app tables
- Cleaner separation of concerns
- Easier backup/restore

**Recommendation:** Use **default `public` schema** for simplicity unless you have specific multi-schema requirements.

---

## 6. Complete Authentication Flow

### 6.1 User Registration Flow

```
┌─────────┐         ┌──────────┐         ┌────────────┐         ┌──────────┐
│ Browser │         │ Next.js  │         │ Better Auth│         │PostgreSQL│
└────┬────┘         └────┬─────┘         └─────┬──────┘         └────┬─────┘
     │                   │                     │                      │
     │  POST /api/auth/signup                 │                      │
     ├──────────────────>│                     │                      │
     │  {email, password}│                     │                      │
     │                   │  Forward request    │                      │
     │                   ├────────────────────>│                      │
     │                   │                     │  Hash password       │
     │                   │                     │  (Argon2id)          │
     │                   │                     │                      │
     │                   │                     │  INSERT INTO user    │
     │                   │                     ├─────────────────────>│
     │                   │                     │                      │
     │                   │                     │  INSERT INTO account │
     │                   │                     ├─────────────────────>│
     │                   │                     │  (with password hash)│
     │                   │                     │                      │
     │                   │                     │<─────────────────────┤
     │                   │                     │  User created        │
     │                   │                     │                      │
     │                   │                     │  CREATE session      │
     │                   │                     ├─────────────────────>│
     │                   │                     │                      │
     │                   │<────────────────────┤                      │
     │                   │  Set-Cookie: session_token                │
     │<──────────────────┤                     │                      │
     │  200 OK           │                     │                      │
     │  Cookie set       │                     │                      │
```

### 6.2 User Login Flow

```
┌─────────┐         ┌──────────┐         ┌────────────┐         ┌──────────┐
│ Browser │         │ Next.js  │         │ Better Auth│         │PostgreSQL│
└────┬────┘         └────┬─────┘         └─────┬──────┘         └────┬─────┘
     │                   │                     │                      │
     │  POST /api/auth/signin                 │                      │
     ├──────────────────>│                     │                      │
     │  {email, password}│                     │                      │
     │                   │  Forward request    │                      │
     │                   ├────────────────────>│                      │
     │                   │                     │  SELECT * FROM user  │
     │                   │                     ├─────────────────────>│
     │                   │                     │  WHERE email=?       │
     │                   │                     │                      │
     │                   │                     │<─────────────────────┤
     │                   │                     │  User data           │
     │                   │                     │                      │
     │                   │                     │  SELECT password     │
     │                   │                     │  FROM account        │
     │                   │                     ├─────────────────────>│
     │                   │                     │                      │
     │                   │                     │<─────────────────────┤
     │                   │                     │  Password hash       │
     │                   │                     │                      │
     │                   │                     │  Verify password     │
     │                   │                     │  (Argon2id)          │
     │                   │                     │                      │
     │                   │                     │  CREATE session      │
     │                   │                     ├─────────────────────>│
     │                   │                     │                      │
     │                   │<────────────────────┤                      │
     │                   │  Set-Cookie: session_token                │
     │<──────────────────┤                     │                      │
     │  200 OK           │                     │                      │
     │  Cookie set       │                     │                      │
```

### 6.3 API Request Flow (Cookie → JWT → Backend)

```
┌─────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────┐
│ Browser │     │ Next.js API  │     │ FastAPI      │     │PostgreSQL│
│         │     │ Proxy        │     │ Backend      │     │          │
└────┬────┘     └──────┬───────┘     └──────┬───────┘     └────┬─────┘
     │                 │                    │                   │
     │  GET /api/proxy/tasks                │                   │
     ├────────────────>│                    │                   │
     │  Cookie: session_token               │                   │
     │                 │                    │                   │
     │                 │  Extract cookie    │                   │
     │                 │  session_token     │                   │
     │                 │                    │                   │
     │                 │  GET /api/{user_id}/tasks             │
     │                 ├───────────────────>│                   │
     │                 │  Authorization:    │                   │
     │                 │  Bearer {token}    │                   │
     │                 │                    │  Decode JWT       │
     │                 │                    │  Extract user_id  │
     │                 │                    │                   │
     │                 │                    │  Verify user_id   │
     │                 │                    │  matches URL      │
     │                 │                    │                   │
     │                 │                    │  SELECT * FROM    │
     │                 │                    │  tasks            │
     │                 │                    ├──────────────────>│
     │                 │                    │  WHERE user_id=?  │
     │                 │                    │                   │
     │                 │                    │<──────────────────┤
     │                 │                    │  Task data        │
     │                 │<───────────────────┤                   │
     │                 │  200 OK            │                   │
     │                 │  {tasks: [...]}    │                   │
     │<────────────────┤                    │                   │
     │  200 OK         │                    │                   │
     │  {tasks: [...]} │                    │                   │
```

### 6.4 Session Validation Flow

```
┌─────────┐         ┌──────────┐         ┌────────────┐         ┌──────────┐
│ Browser │         │ Next.js  │         │ Better Auth│         │PostgreSQL│
└────┬────┘         └────┬─────┘         └─────┬──────┘         └────┬─────┘
     │                   │                     │                      │
     │  GET /dashboard   │                     │                      │
     ├──────────────────>│                     │                      │
     │  Cookie: session_token                 │                      │
     │                   │                     │                      │
     │                   │  getSession()       │                      │
     │                   ├────────────────────>│                      │
     │                   │  session_token      │                      │
     │                   │                     │  SELECT * FROM       │
     │                   │                     │  session             │
     │                   │                     ├─────────────────────>│
     │                   │                     │  WHERE token=?       │
     │                   │                     │                      │
     │                   │                     │<─────────────────────┤
     │                   │                     │  Session data        │
     │                   │                     │                      │
     │                   │                     │  Check expiration    │
     │                   │                     │  expiresAt > now()   │
     │                   │                     │                      │
     │                   │                     │  SELECT * FROM user  │
     │                   │                     ├─────────────────────>│
     │                   │                     │  WHERE id=?          │
     │                   │                     │                      │
     │                   │                     │<─────────────────────┤
     │                   │                     │  User data           │
     │                   │<────────────────────┤                      │
     │                   │  {user, session}    │                      │
     │<──────────────────┤                     │                      │
     │  200 OK           │                     │                      │
     │  Render dashboard │                     │                      │
```

---

## 7. Implementation Decisions

### 7.1 Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Auth Library** | Better Auth | Modern, TypeScript-native, flexible |
| **Session Strategy** | Database Sessions | Secure, supports revocation |
| **JWT Library** | PyJWT | Actively maintained, FastAPI recommended |
| **Token Verification** | Dependency Injection | Granular control, testable |
| **Cookie Attributes** | httpOnly, secure, sameSite=lax | Industry best practices |
| **CORS** | Allow credentials with explicit origins | Secure cookie-based auth |
| **Secret Management** | Environment variables | Never commit secrets |

### 7.2 Security Decisions

1. **Use httpOnly Cookies for Session Tokens**
   - Prevents XSS attacks
   - Industry standard for web authentication

2. **JWT Tokens for API Authentication**
   - Stateless verification on backend
   - No database lookup for every request
   - Standard Bearer token format

3. **Next.js API Proxy for Cookie→Header Translation**
   - Keeps httpOnly cookies secure
   - Backend receives standard Bearer tokens
   - Clean separation of concerns

4. **User Isolation Enforcement**
   - Verify user_id in URL matches JWT token
   - 401 for missing/invalid auth
   - 403 for valid auth but wrong resource

5. **CORS with Explicit Origins**
   - No wildcard `*` when using credentials
   - Specify exact allowed origins
   - Enable `credentials: true`

### 7.3 Database Decisions

1. **Let Better Auth Manage Auth Tables**
   - Use CLI migrations
   - Standard schema structure
   - Future-proof for plugins

2. **Foreign Key to Better Auth User Table**
   - `tasks.user_id` references `user.id`
   - Referential integrity
   - Cascade delete for cleanup

3. **PostgreSQL with Neon**
   - Serverless, auto-scaling
   - Reliable connection pooling
   - Compatible with Better Auth

### 7.4 Token Configuration

| Parameter | Value | Justification |
|-----------|-------|---------------|
| **Session Expiration** | 7 days | Balance security/UX |
| **JWT Expiration** | 1 hour | Short-lived for API access |
| **Token Algorithm** | HS256 | Symmetric, fast, sufficient for this use case |
| **Token Secret** | 256-bit (32 bytes) | Minimum for HS256 security |
| **Subject Claim** | User ID | Standard JWT practice |

### 7.5 API Design Decisions

1. **RESTful Endpoints with User ID Prefix**
   - Pattern: `/api/{user_id}/tasks`
   - Clear ownership
   - URL-based authorization check

2. **Bearer Token in Authorization Header**
   - Standard HTTP authentication
   - Compatible with API testing tools
   - Clear authentication flow

3. **Consistent Error Responses**
   - 401: Authentication required
   - 403: Insufficient permissions
   - Standard error format

### 7.6 File Structure

**Frontend (Next.js):**
```
frontend/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth/[...all]/route.ts  # Better Auth handler
│   │   │   └── proxy/[...path]/route.ts # API proxy
│   │   ├── (authenticated)/
│   │   │   └── tasks/page.tsx
│   │   └── layout.tsx
│   ├── lib/
│   │   ├── auth.ts          # Better Auth server config
│   │   └── auth-client.ts   # Better Auth client
│   └── components/
├── .env.local
└── package.json
```

**Backend (FastAPI):**
```
backend/
├── app/
│   ├── main.py              # FastAPI app + CORS
│   ├── auth.py              # JWT verification dependencies
│   ├── models/
│   │   ├── user.py          # User model (Better Auth tables)
│   │   └── task.py          # Task model
│   ├── routes/
│   │   └── tasks.py         # Task CRUD endpoints
│   └── schemas/
│       └── task.py          # Pydantic schemas
├── .env
└── requirements.txt
```

---


## 7. Implementation Decisions Summary

| Decision Point | Chosen Solution | Rationale |
|----------------|----------------|-----------|
| Auth Library | Better Auth with JWT plugin | Modern, Next.js-optimized, automatic table creation |
| JWT Library (Python) | PyJWT | Active maintenance, Python 3.10+ compatible (python-jose abandoned) |
| JWT Verification Pattern | FastAPI dependency injection | Granular control, testability, selective application |
| Cookie Storage | httpOnly, secure, sameSite=lax | XSS protection, HTTPS only, CSRF mitigation |
| Token Expiration | 7 days | Balance security and UX (no refresh tokens) |
| CORS Strategy | Explicit origins with credentials | Required for httpOnly cookies (cannot use wildcard) |
| Error Handling | 401 for auth, 403 for authz | Standard HTTP semantics |
| Database Tables | Better Auth automatic creation | Reduces manual errors, ensures compatibility |
| API Proxy Pattern | Next.js Edge runtime | Fast, server-side cookie reading, simple forwarding |
| User ID Claim | JWT 'sub' field | Standard claim for subject/user identification |

## 8. Next Steps for Implementation

1. **Phase 1: Frontend Better Auth Setup**
   - Install `better-auth` and `@better-auth/jwt` packages
   - Configure Better Auth in `frontend/src/lib/auth.ts`
   - Create API routes at `frontend/src/app/api/auth/[...all]/route.ts`
   - Set up database connection and run migrations

2. **Phase 2: Frontend UI Components**
   - Create login form at `frontend/src/app/(auth)/login/page.tsx`
   - Create signup form at `frontend/src/app/(auth)/signup/page.tsx`
   - Create logout button component
   - Set up protected route wrapper

3. **Phase 3: Frontend API Proxy**
   - Implement proxy at `frontend/src/app/api/proxy/[...path]/route.ts`
   - Handle all HTTP methods (GET, POST, PUT, DELETE, PATCH)
   - Add error handling and response forwarding

4. **Phase 4: Backend JWT Verification**
   - Install PyJWT package
   - Create JWT dependencies at `backend/app/dependencies/auth.py`
   - Update task routes to use auth dependencies
   - Configure CORS with credentials

5. **Phase 5: Testing**
   - Test signup creates user and logs in
   - Test login issues valid JWT
   - Test logout clears token
   - Test invalid token returns 401
   - Test mismatched user_id returns 403
   - Test session persistence across refreshes
   - Test protected routes redirect to login

---

## Summary of Key Recommendations

### For Better Auth (Frontend)

1. **Use Database Sessions** (not stateless)
2. **Configure httpOnly, secure, sameSite=lax cookies**
3. **Install JWT plugin** for API token generation
4. **Set session expiration to 7 days**
5. **Use BETTER_AUTH_SECRET from environment**

### For Next.js API Proxy

1. **Create proxy route** to forward cookies as Authorization headers
2. **Extract session_token from httpOnly cookie**
3. **Forward as `Authorization: Bearer {token}`**
4. **Handle all HTTP methods (GET, POST, PUT, DELETE, PATCH)**
5. **Return 401 if session_token missing**

### For FastAPI Backend

1. **Install PyJWT** (not python-jose)
2. **Use dependency injection** for JWT verification
3. **Extract user_id from `sub` claim**
4. **Verify user_id matches URL parameter**
5. **Return 401 for auth failures, 403 for permission denials**
6. **Configure CORS with explicit origins and credentials=True**

### For Database

1. **Run Better Auth CLI migrations** (`npx better-auth migrate`)
2. **Let Better Auth create: user, session, account, verification tables**
3. **Create tasks table with foreign key** to `user.id`
4. **Use PostgreSQL with Neon** serverless database

### For Security

1. **Never commit .env files**
2. **Use 256-bit random secrets**
3. **Same secret for frontend and backend**
4. **Enable CORS credentials with explicit origins**
5. **Use httpOnly cookies for session tokens**
6. **Use Bearer tokens for API authentication**
7. **Validate token expiration**
8. **Enforce user isolation on all endpoints**

---

## References

### Better Auth Documentation
- [Better Auth Official Docs](https://www.better-auth.com/docs)
- [Next.js Integration](https://www.better-auth.com/docs/integrations/next)
- [JWT Plugin](https://www.better-auth.com/docs/plugins/jwt)
- [Session Management](https://www.better-auth.com/docs/concepts/session-management)
- [Cookies Configuration](https://www.better-auth.com/docs/concepts/cookies)
- [PostgreSQL Adapter](https://www.better-auth.com/docs/adapters/postgresql)
- [Database Migrations](https://www.better-auth.com/docs/concepts/cli)

### Next.js Documentation
- [Next.js App Router](https://nextjs.org/docs/app)
- [Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route)
- [Cookies Function](https://nextjs.org/docs/app/api-reference/functions/cookies)

### FastAPI Documentation
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security)
- [OAuth2 with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt)
- [CORS Middleware](https://fastapi.tiangolo.com/tutorial/cors)
- [Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies)

### PyJWT Documentation
- [PyJWT Official Docs](https://pyjwt.readthedocs.io)
- [Encoding Tokens](https://pyjwt.readthedocs.io/en/stable/usage.html#encoding-decoding-tokens-with-hs256)
- [Decoding and Verification](https://pyjwt.readthedocs.io/en/stable/usage.html#reading-the-claimset-without-validation)
- [Exception Handling](https://pyjwt.readthedocs.io/en/stable/api.html#exceptions)

### Security Standards
- [RFC 7519 - JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [RFC 7235 - HTTP Authentication](https://datatracker.ietf.org/doc/html/rfc7235)
- [RFC 6749 - OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc6749)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

---

**Document Version:** 1.0
**Last Updated:** 2026-02-03
**Prepared By:** Claude Code (Sonnet 4.5) + Research Agent
**Status:** Ready for Implementation
