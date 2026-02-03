# Feature Specification: Fix Better Auth Integration

**Feature Branch**: `004-fix-better-auth-integration`
**Created**: 2026-02-03
**Status**: Draft
**Input**: User description: "Fix Better Auth frontend build errors and backend authentication test failures"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer Builds Frontend Successfully (Priority: P1)

As a developer, I need the frontend to build without errors so that I can deploy the application and continue development work.

**Why this priority**: Without a successful build, the application cannot run, blocking all development and deployment. This is a critical blocker affecting the entire team.

**Independent Test**: Run `npm run build` in the frontend directory. The build must complete with zero errors and generate production-ready artifacts in the `.next` directory.

**Acceptance Scenarios**:

1. **Given** the Better Auth client is properly configured, **When** a developer runs `npm run build`, **Then** the build completes successfully with zero Turbopack errors
2. **Given** all auth components use the correct Better Auth API, **When** TypeScript compilation runs, **Then** no import or type errors occur
3. **Given** the build artifacts are generated, **When** the developer inspects the output, **Then** all JavaScript bundles are created without warnings

---

### User Story 2 - Developer Runs Backend Tests Successfully (Priority: P1)

As a developer, I need all backend authentication tests to pass so that I can verify the API security layer works correctly before deployment.

**Why this priority**: Authentication is critical for security. Failed tests indicate potential security vulnerabilities or broken JWT verification that could expose user data.

**Independent Test**: Run `pytest` in the backend directory. All authentication tests (19 tests) and database tests (14 tests) must pass with green output.

**Acceptance Scenarios**:

1. **Given** the backend authentication middleware is implemented, **When** a developer runs authentication tests, **Then** all 19 auth tests pass without failures
2. **Given** test mocks properly simulate FastAPI dependencies, **When** JWT token validation tests run, **Then** valid tokens are accepted and invalid tokens are rejected correctly
3. **Given** all tests complete, **When** the developer reviews the output, **Then** there are zero deprecation warnings or test infrastructure errors

---

### User Story 3 - End User Authenticates Successfully (Priority: P2)

As an end user, I need to sign up, log in, and access protected features so that I can use the todo application securely.

**Why this priority**: While fixing tests and builds are critical infrastructure tasks (P1), the ultimate goal is ensuring the authentication flow works for end users.

**Independent Test**: Start both frontend and backend servers. Navigate to `/auth/signup`, create an account, log in, access protected `/dashboard` route, perform CRUD operations on tasks, and log out successfully.

**Acceptance Scenarios**:

1. **Given** a new user visits the signup page, **When** they enter valid credentials and submit, **Then** their account is created and they are redirected to the dashboard
2. **Given** an existing user visits the login page, **When** they enter correct credentials, **Then** they receive a JWT token in an httpOnly cookie and can access protected routes
3. **Given** an authenticated user is on the dashboard, **When** they create a task, **Then** the task is saved with their user_id and only visible to them
4. **Given** an authenticated user clicks logout, **When** the logout completes, **Then** their session is cleared and they are redirected to the login page
5. **Given** a user's session has expired, **When** they attempt to access a protected route, **Then** they are redirected to login with an appropriate message

---

### Edge Cases

- **JWT Token Expiry During Active Session**: When a user's JWT token expires while actively using the application, the system must redirect them to the login page with a "Session expired" message displayed
- **Malformed JWT Tokens**: System must reject malformed JWT tokens in API requests with 401 Unauthorized response
- **Missing/Mismatched BETTER_AUTH_SECRET**: If the environment variable is missing or mismatched between frontend and backend, JWT verification will fail and all authentication requests will be rejected
- **Build-time Import Errors**: Better Auth import errors in deeply nested components must be caught during TypeScript compilation and reported as build errors
- **Incorrect Test Mocks**: Backend tests with incorrect FastAPI dependency injection mocks must fail with clear error messages indicating the mocking issue
- **Concurrent Authentication Requests**: System must handle concurrent authentication requests during testing without race conditions or state corruption

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Frontend MUST import Better Auth client functionality from `better-auth/react` using `createAuthClient` instead of individual hook imports
- **FR-002**: All frontend authentication components MUST use `authClient.signIn.email()`, `authClient.signUp.email()`, and `authClient.signOut()` methods instead of deprecated hooks
- **FR-003**: Session state checking MUST use `authClient.useSession()` hook in all React components that need authentication status
- **FR-004**: Backend authentication tests MUST properly mock FastAPI dependency injection for JWT verification
- **FR-005**: Backend tests MUST generate valid JWT tokens with correct claims (sub, email, exp, iat, iss) matching the Better Auth format
- **FR-006**: All authentication tests MUST verify user isolation by ensuring cross-user access attempts return 403 Forbidden
- **FR-007**: Frontend build process MUST complete without TypeScript errors, Turbopack errors, or missing import warnings
- **FR-008**: Backend test suite MUST maintain existing database test coverage (14/14 tests passing) while fixing authentication tests
- **FR-009**: JWT token flow MUST work end-to-end: frontend login → httpOnly cookie → backend verification → user-specific data retrieval
- **FR-010**: Logout functionality MUST clear authentication state, invalidate sessions, and redirect users appropriately
- **FR-011**: System MUST implement structured logging to files for all authentication events (sign-in, sign-out, token validation, session checks) in both development and production environments to enable troubleshooting and audit trails

### Key Entities *(include if feature involves data)*

- **Auth Client**: Central authentication client instance created via `createAuthClient` from `better-auth/react`, providing sign-in, sign-up, sign-out, and session management methods
- **JWT Token**: JSON Web Token containing user claims (sub: user_id, email, exp, iat, iss: "better-auth") used for stateless authentication
- **Session State**: Reactive authentication state exposed via `authClient.useSession()` hook, containing user data and loading/error states
- **Test Mock**: FastAPI dependency override patterns that simulate authenticated users for testing protected endpoints

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Frontend build completes in under 60 seconds with zero errors and produces deployable artifacts
- **SC-002**: All 33 backend tests (14 database + 19 authentication) pass with 100% success rate (tests may retry up to 3 times on failure to handle intermittent issues)
- **SC-003**: Authentication flow from signup to logout completes successfully in under 5 minutes during manual testing
- **SC-004**: Developers can run the entire test suite (`npm run build && pytest`) without any failures or warnings
- **SC-005**: User isolation is verified in tests with 100% of cross-user access attempts correctly rejected
- **SC-006**: JWT token verification works correctly with 100% of valid tokens accepted and 100% of invalid/expired tokens rejected
- **SC-007**: Zero deprecation warnings or error messages appear in test output or build logs

## Assumptions

1. Better Auth version 1.4.18 is the target version (as indicated in package.json)
2. The `BETTER_AUTH_SECRET` environment variable is correctly configured and identical in both frontend and backend
3. The database connection for Better Auth (Neon PostgreSQL) is properly configured and accessible
4. Existing database schema for Better Auth tables (users, sessions, etc.) is already in place from previous setup
5. The FastAPI backend uses standard dependency injection patterns for authentication middleware
6. The test environment has access to the same environment variables as the production environment
7. No breaking changes are required to the existing authentication middleware or JWT verification logic
8. The frontend uses Next.js 16+ with App Router (as confirmed in project structure)
9. TypeScript strict mode is enabled and must be satisfied by all code changes

## Out of Scope

- Upgrading Better Auth to a different major version
- Implementing new authentication features (OAuth, magic links, 2FA, etc.)
- Refactoring the authentication architecture or switching to a different auth library
- Performance optimization of authentication flows beyond fixing breaking issues
- Adding new test coverage beyond fixing existing failing tests
- UI/UX improvements to authentication pages
- Internationalization (i18n) for authentication error messages
- Rate limiting or brute force protection enhancements
- Audit logging improvements for authentication events
- Migration of existing user accounts or session data

## Dependencies

- **Better Auth library**: Version 1.4.18 with updated API patterns (createAuthClient, authClient methods)
- **Environment configuration**: `BETTER_AUTH_SECRET` must be set and matching in both frontend and backend `.env` files
- **Database schema**: Better Auth database tables must exist in Neon PostgreSQL
- **Test infrastructure**: pytest, FastAPI TestClient, and React Testing Library must be properly configured
- **Build tools**: Next.js 16+ Turbopack, TypeScript compiler, and Node.js environment

## Security Considerations

- JWT tokens must remain in httpOnly cookies to prevent XSS attacks
- Token signatures must be verified using the shared `BETTER_AUTH_SECRET` on every backend request
- Test mocks must not bypass security checks or create vulnerabilities in production code
- User isolation must be strictly enforced with every database query filtered by authenticated user_id
- Expired or invalid tokens must be rejected immediately with appropriate 401 Unauthorized responses
- Cross-user access attempts must return 403 Forbidden to prevent information disclosure

## Clarifications

### Session 2026-02-03

- Q: What happens when a user's JWT token expires while they are actively using the application? → A: Redirect to login page with a "Session expired" message displayed to user
- Q: How should the test suite handle flaky tests in CI/CD to prevent intermittent failures from blocking deployments? → A: Allow up to 3 automatic retries before considering test failed
- Q: What level of logging/debugging output is expected during development to help troubleshoot authentication issues? → A: Structured logging to files for all authentication events regardless of environment

## Notes

This is a critical bug fix feature that unblocks development and deployment. The specification focuses on restoring functionality that was broken by Better Auth API changes, specifically the migration from individual hooks (`useSignIn`, `useSignOut`, `useSignUp`) to a unified `createAuthClient` pattern with method-based authentication.

The root cause has been identified:
- **Frontend**: Components import non-existent hooks from `better-auth/react`
- **Backend**: Test infrastructure uses incorrect patterns for FastAPI dependency mocking

All fixes must maintain backward compatibility with existing authentication flows and data structures. No breaking changes to the user experience or API contracts are permitted.
