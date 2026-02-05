# Research: FastAPI Backend with CRUD Operations & JWT Security

## Technology Choices

### Decision: FastAPI Framework
**Rationale**: FastAPI provides automatic API documentation (Swagger/OpenAPI), built-in validation with Pydantic, excellent performance through Starlette, and strong typing support. It's perfect for building secure, well-documented APIs with minimal code.

**Alternatives considered**:
- Flask: More manual work required for validation and documentation
- Django: Overkill for this simple API service
- Express.js: Would require switching to Node.js ecosystem

### Decision: SQLModel for ORM
**Rationale**: SQLModel combines the power of SQLAlchemy with Pydantic validation, allowing us to use the same models for both database operations and API validation. It's developed by the same creator as FastAPI and integrates seamlessly.

**Alternatives considered**:
- SQLAlchemy Core: More verbose, less validation integration
- Tortoise ORM: Async-focused but less mature than SQLModel
- Peewee: Simpler but lacks Pydantic integration

### Decision: Better Auth for JWT
**Rationale**: Better Auth is specifically designed to work with Next.js and provides seamless JWT token handling. It's lightweight, secure, and integrates well with both frontend and backend applications.

**Alternatives considered**:
- Auth0: More complex for this use case, adds external dependency
- PyJWT directly: Requires more manual setup and maintenance
- FastAPI's OAuth2PasswordBearer: More work for a simple JWT implementation

## Security Patterns

### Decision: JWT Token Verification Pattern
**Rationale**: Using FastAPI dependencies to verify JWT tokens ensures that authentication happens consistently across all endpoints. The dependency will extract user identity and compare with URL parameters to enforce user isolation.

**Implementation pattern**:
- Create `verify_jwt` dependency that validates token and extracts user_id
- Compare extracted user_id with URL parameter user_id
- Return appropriate HTTP exceptions for failures

### Decision: Database Session Management
**Rationale**: Using FastAPI dependencies for database session management ensures proper connection handling, automatic cleanup, and consistent error handling across all endpoints.

**Implementation pattern**:
- Create `get_session` dependency that provides database session
- Use try/finally or context managers to ensure session closure
- Handle connection errors gracefully

## API Design Decisions

### Decision: RESTful URL Structure
**Rationale**: Using `/api/{user_id}/tasks` and `/api/{user_id}/tasks/{id}` follows REST conventions while enforcing user context in the URL, which is essential for data isolation.

**Alternatives considered**:
- Using headers for user context: Less RESTful and harder to validate
- Global task IDs with hidden user mapping: Doesn't make user context explicit

### Decision: Separate PATCH Endpoint for Completion Toggle
**Rationale**: Having a dedicated endpoint `/api/{user_id}/tasks/{id}/complete` makes the completion toggle operation explicit and clear, while keeping full updates separate in the PUT endpoint.

**Alternatives considered**:
- Using PUT with partial updates: Could accidentally update other fields
- Using POST to /complete: Less RESTful than PATCH for state changes

## Error Handling Approach

### Decision: Standard HTTPException Pattern
**Rationale**: FastAPI's HTTPException with proper status codes provides consistent error responses that are easy for frontend applications to handle appropriately.

**Implementation pattern**:
- 401 for authentication failures
- 403 for authorization failures (wrong user context)
- 404 for not found resources
- 422 for validation errors (handled automatically by FastAPI)
- 500 for internal server errors

## CORS Configuration

### Decision: Environment-Based Origins
**Rationale**: Configuring CORS origins through environment variables allows for different configurations in development, staging, and production environments while supporting the frontend integration requirement.

**Implementation pattern**:
- Use environment variable for allowed origins
- Support credentials in CORS configuration for httpOnly cookie access
- Configure appropriate headers for frontend-backend communication