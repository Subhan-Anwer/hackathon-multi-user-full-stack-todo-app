# Tasks: Database Schema & SQLModel Implementation

## Phase 1: Setup (Project Initialization)

- [X] T001 Create backend directory structure: `backend/app/models`, `backend/app/db`, `backend/app/routes`, `backend/app/schemas`
- [X] T002 Create backend requirements file with dependencies: sqlmodel, pydantic, psycopg2-binary, fastapi, uvicorn, python-multipart, python-jose[cryptography], passlib[bcrypt], python-dotenv
- [X] T003 [P] Create pyproject.toml file in backend directory with project metadata and dependencies
- [X] T004 Create backend .env file template with DATABASE_URL and BETTER_AUTH_SECRET placeholders

## Phase 2: Foundational (Blocking Prerequisites)

- [X] T010 [P] Create virtual environment setup documentation in backend/README.md
- [ ] T011 Install uv package manager and configure for backend project
- [X] T012 [P] Set up database connection module in backend/app/db/db.py with SQLModel engine
- [X] T013 [P] Create base SQLModel configuration with proper database URL handling
- [X] T014 Create session dependency for FastAPI in backend/app/db/db.py
- [X] T015 [P] Create database initialization function to create all tables

## Phase 3: [US1] Create Tasks with User Isolation

**Goal**: Implement the core Task model that allows users to create tasks with proper user isolation and validation.

**Independent Test**: Can be fully tested by creating tasks for different users and verifying that each user can only access their own tasks. Delivers the fundamental value of a personalized todo list.

**Tasks**:
- [X] T020 [P] [US1] Create Task model in backend/app/models/models.py with all 7 required fields
- [X] T021 [US1] Implement field constraints: id as primary key, user_id as non-null foreign key, title max 200 chars, description max 1000 chars
- [X] T022 [US1] Add validation rules for title and description character limits in Task model
- [X] T023 [P] [US1] Implement automatic timestamp generation for created_at and updated_at fields
- [X] T024 [US1] Add foreign key relationship to users table with cascade delete option
- [X] T025 [P] [US1] Create Pydantic schemas for task validation in backend/app/schemas/task_schemas.py
- [X] T026 [US1] Implement create task functionality with user_id validation
- [X] T027 [US1] Add input validation for task creation (title length, description length)
- [ ] T028 [US1] Test task creation with valid data and verify user_id association
- [ ] T029 [US1] Test task creation with invalid data (e.g., title exceeding 200 characters) and verify rejection

## Phase 4: [US2] View and Manage Personal Tasks

**Goal**: Enable users to retrieve their own tasks while maintaining privacy and data isolation from other users.

**Independent Test**: Can be tested by creating multiple users with various tasks and verifying that each user only sees their own tasks when querying the system.

**Tasks**:
- [X] T035 [P] [US2] Create database query functions to retrieve tasks by user_id in backend/app/models/models.py
- [X] T036 [US2] Implement get all tasks for user functionality with proper filtering
- [X] T037 [P] [US2] Create API endpoint to retrieve user's task list in backend/app/routes/tasks.py
- [X] T038 [US2] Add user_id validation to ensure users can only access their own tasks
- [X] T039 [P] [US2] Implement get single task by ID with user verification
- [X] T040 [US2] Create API endpoint for retrieving specific task by ID
- [X] T041 [P] [US2] Add proper error handling for unauthorized task access attempts
- [ ] T042 [US2] Test that users can only retrieve their own tasks
- [ ] T043 [US2] Test single task access with proper user verification
- [ ] T044 [US2] Verify user isolation by testing cross-user access prevention

## Phase 5: [US3] Update Task Status and Details

**Goal**: Allow users to modify their existing tasks by updating title, description, or completion status while maintaining data integrity.

**Independent Test**: Can be tested by attempting to update tasks with different user accounts and verifying that only the task owner can make modifications.

**Tasks**:
- [X] T050 [P] [US3] Implement update task functionality in backend/app/models/models.py
- [X] T051 [US3] Create API endpoint for updating task details in backend/app/routes/tasks.py
- [X] T052 [P] [US3] Add validation for task updates (title length, description length)
- [X] T053 [US3] Implement completion status toggle functionality
- [X] T054 [P] [US3] Create API endpoint for toggling task completion status
- [X] T055 [US3] Add user verification to update operations to ensure ownership
- [X] T056 [P] [US3] Implement soft delete or mark-as-deleted functionality
- [X] T057 [US3] Create API endpoint for deleting tasks
- [ ] T058 [US3] Test that users can update their own tasks
- [ ] T059 [US3] Test that users cannot update tasks belonging to other users
- [ ] T060 [US3] Test task deletion with proper user verification

## Phase 6: Query Optimization and Indexing

**Goal**: Optimize database queries with proper indexing for efficient user-specific task operations.

**Tasks**:
- [X] T070 [P] Create database indexes on user_id field for efficient user-specific queries
- [X] T071 Create database index on completed field for efficient status filtering
- [X] T072 [P] Create composite index on (user_id, completed) for optimized combined queries
- [X] T073 Implement optimized query patterns for common access patterns (view all, filter completed, filter pending)
- [ ] T074 [P] Test query performance with multiple users and tasks
- [ ] T075 Document query optimization strategies and performance benchmarks

## Phase 7: Polish & Cross-Cutting Concerns

**Tasks**:
- [X] T080 [P] Add comprehensive error handling and logging to all database operations
- [X] T081 Create unit tests for Task model validation and constraints
- [X] T082 [P] Implement integration tests for database operations with PostgreSQL
- [X] T083 Add tests for user data isolation to confirm cross-account access prevention
- [ ] T084 [P] Create documentation for the database schema and API endpoints
- [X] T085 Update project README with database setup and usage instructions
- [X] T086 [P] Add environment variable validation for database connection
- [X] T087 Perform security review to ensure user data isolation is properly enforced
- [ ] T088 [P] Add database migration documentation (though using create_all for now)
- [X] T089 Final integration testing of all user stories together

## Dependencies

**User Story Completion Order**:
1. US1 (Create Tasks) → Must be completed before US2 and US3
2. US2 (View Tasks) → Depends on US1 (needs Task model)
3. US3 (Update Tasks) → Depends on US1 (needs Task model)

**Critical Path**: T001 → T002 → T012 → T020 → T021 → T022 → T026 → T035 → T036 → T050 → T051

## Parallel Execution Examples

**Per User Story**:
- **US1**: T020[T023], T021[T022], T025[T026], T028[T029] (parallel tasks separated by square brackets)
- **US2**: T035[T037], T036[T038], T041[T042], T043[T044]
- **US3**: T050[T052], T051[T054], T055[T057], T058[T059][T060]

## Implementation Strategy

**MVP Scope**: Focus on US1 (Task creation with user isolation) as the minimal viable product that delivers core value.

**Incremental Delivery**:
1. **MVP**: US1 - Users can create tasks with proper user isolation
2. **v1.1**: Add US2 - Users can view their tasks
3. **v1.2**: Add US3 - Users can update/delete tasks
4. **v1.3**: Add optimization and polish

Each increment builds upon the previous one while delivering increasing value to the user.