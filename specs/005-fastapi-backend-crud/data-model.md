# Data Model: FastAPI Backend with CRUD Operations & JWT Security

## Entity: Task

### Fields
- **id**: Integer (Primary Key, Auto-generated)
- **title**: String (Required, Max length: 255)
- **description**: String (Optional, Max length: 1000)
- **completed**: Boolean (Default: False)
- **user_id**: String (Foreign Key, References User.id, Required for user isolation)
- **created_at**: DateTime (Auto-generated, UTC)
- **updated_at**: DateTime (Auto-generated, UTC, Updates on modification)

### Relationships
- **Belongs to**: User (many tasks to one user relationship)

### Validation Rules
- **title**: Required, minimum 1 character, maximum 255 characters
- **description**: Optional, maximum 1000 characters
- **completed**: Boolean, default false
- **user_id**: Required, must exist in users table (enforced by foreign key)

### State Transitions
- **New Task**: created_at set, completed = false
- **Updated Task**: updated_at updated to current timestamp
- **Completed Task**: completed = true (via toggle endpoint)
- **Reopened Task**: completed = false (via toggle endpoint)

## Entity: User (Reference Only)

### Fields
- **id**: String (Primary Key, Provided by Better Auth)
- **email**: String (Unique, Provided by Better Auth)
- **created_at**: DateTime (Provided by Better Auth)

### Relationship Constraints
- All tasks must have a valid user_id that exists in the users table
- Users can only access tasks where user_id matches their own id

## Indexes
- **idx_tasks_user_id**: Index on user_id for efficient filtering by user
- **idx_tasks_completed**: Index on completed for efficient querying of completed/incomplete tasks

## Constraints
- **Foreign Key Constraint**: user_id must reference valid user
- **Non-null Constraints**: id, title, user_id, created_at, updated_at cannot be null
- **Check Constraint**: title length must be 1-255 characters