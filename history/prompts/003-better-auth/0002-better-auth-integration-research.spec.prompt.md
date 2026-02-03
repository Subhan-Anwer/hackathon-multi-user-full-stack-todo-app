---
id: 0002
title: Better Auth Integration Research for Next.js and FastAPI
stage: spec
date: 2026-02-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-better-auth
branch: 003-better-auth
user: subhan
command: research
labels: ["better-auth", "jwt", "nextjs", "fastapi", "authentication", "security", "cors", "database-schema"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - research.md
tests:
  - N/A (Research documentation)
---

## Prompt

Research and document the following for Better Auth integration with Next.js and FastAPI:

1. **Better Auth Library Architecture**:
   - How Better Auth handles JWT token generation
   - JWT plugin configuration and payload structure
   - httpOnly cookie configuration (name, attributes, security flags)
   - Session management patterns

2. **Next.js API Proxy Pattern**:
   - Best practices for server-side cookie reading in Next.js App Router
   - How to forward cookies as Authorization headers to backend
   - Handling all HTTP methods (GET, POST, PUT, DELETE, PATCH)
   - Error handling and response forwarding

3. **FastAPI JWT Verification**:
   - PyJWT vs python-jose comparison (which is better for FastAPI?)
   - Middleware vs dependency injection for JWT verification
   - Extracting user_id from JWT payload ('sub' field standard)
   - Error responses (401 Unauthorized vs 403 Forbidden)

4. **Security Best Practices**:
   - CORS configuration for cookie credentials
   - Cookie attributes (httpOnly, secure, sameSite)
   - JWT secret management and rotation
   - Token expiration handling

5. **Database Schema for Users**:
   - Does Better Auth create users table automatically?
   - Required fields (id, email, password_hash)
   - Integration with existing PostgreSQL schema

Output a comprehensive research.md file with decisions, rationale, and code examples for each area.

## Response snapshot

Conducted comprehensive research using Context7 MCP server to query official documentation for:
- Better Auth (/llmstxt/better-auth_llms_txt) - JWT plugin, session management, cookies, database schema
- Next.js (/websites/nextjs, /vercel/next.js) - App Router, cookies API, proxy patterns
- FastAPI (/websites/fastapi_tiangolo) - JWT authentication, CORS, security
- PyJWT (/jpadilla/pyjwt) - Token encoding/decoding, verification

Created comprehensive 56KB research.md document with:

**Section 1: Better Auth Architecture**
- JWT plugin is optional, primarily uses session-based auth
- Detailed JWT payload structure (sub, iss, aud, exp, iat)
- httpOnly cookie defaults (secure, sameSite=lax)
- Database vs stateless session strategies

**Section 2: Next.js API Proxy Pattern**
- Edge runtime vs Node.js runtime comparison
- Server-side cookie reading with cookies() from next/headers
- Complete proxy implementation for all HTTP methods
- Error handling and response forwarding patterns

**Section 3: FastAPI JWT Verification**
- **Decision: Use PyJWT** (python-jose is abandoned since 2021)
- **Decision: Dependency injection over middleware** for JWT verification
- Standard 'sub' claim for user_id extraction
- Proper 401 vs 403 error handling with WWW-Authenticate headers

**Section 4: Security Best Practices**
- CORS configuration with credentials=True and explicit origins
- Cookie security attributes (httpOnly, secure, sameSite)
- JWT secret generation (256-bit minimum) and rotation strategies
- Token expiration handling (1h for access tokens, 7d for sessions)

**Section 5: Database Schema**
- Better Auth CLI automatically creates 4 core tables (user, session, account, verification)
- Password hash stored in account table (not user table)
- Argon2id hashing by default
- Foreign key integration with tasks table

**Section 6: Complete Authentication Flow**
- Registration flow diagram
- Login flow diagram
- API request flow (Cookie → JWT → Backend)
- Session validation flow

**Section 7: Implementation Decisions**
- Architecture decisions table
- Security decisions with rationale
- Database approach (let Better Auth manage auth tables)
- Token configuration parameters
- File structure recommendations

All decisions backed by official documentation with code examples and security rationale.

## Outcome

- ✅ Impact: Comprehensive research document provides complete blueprint for Better Auth integration with Next.js and FastAPI, covering all authentication flows, security configurations, and implementation patterns
- 🧪 Tests: N/A (Research documentation with code examples)
- 📁 Files: Created research.md (56KB, ~1000 lines) with 7 major sections, 50+ code examples, 4 flow diagrams
- 🔁 Next prompts:
  1. Implement Better Auth server configuration in Next.js
  2. Create JWT plugin configuration
  3. Implement Next.js API proxy route
  4. Set up FastAPI JWT verification with PyJWT
  5. Configure CORS middleware in FastAPI
- 🧠 Reflection: Using Context7 MCP server provided high-quality, official documentation from Better Auth, Next.js, FastAPI, and PyJWT sources. Research revealed key insights: (1) Better Auth is primarily session-based, JWT plugin is optional; (2) python-jose is abandoned, PyJWT is now standard; (3) Dependency injection is better than middleware for JWT verification; (4) proper 401 vs 403 distinction is critical for API security

## Evaluation notes (flywheel)

- Failure modes observed: None - Context7 MCP server provided comprehensive, up-to-date documentation
- Graders run and results (PASS/FAIL): N/A (Research task)
- Prompt variant (if applicable): Used Context7 MCP server instead of WebSearch for authoritative documentation sources
- Next experiment (smallest change to try): Begin implementation phase with Better Auth server configuration, validating research findings against actual integration requirements
