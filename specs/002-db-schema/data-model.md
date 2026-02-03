# Data Model: Task Entity for Todo Application

## Entity: Task

### Fields

| Field Name | Type | Constraints | Description |
|------------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique identifier for each task |
| user_id | UUID/String | Not Null, Foreign Key to users.id | Links task to authenticated user account |
| title | String(200) | Not Null, Max 200 chars | Task title/description in brief |
| description | Text(String(1000)) | Nullable, Max 1000 chars | Detailed task description |
| completed | Boolean | Not Null, Default False | Completion status of the task |
| created_at | DateTime | Not Null, Auto-generated | Timestamp when task was created |
| updated_at | DateTime | Not Null, Auto-generated | Timestamp when task was last updated |

### Relationships

- **Foreign Key**: `Task.user_id` → `users.id` (ON DELETE CASCADE)
  - Ensures user data isolation
  - Automatically removes tasks when user account is deleted
  - Maintains referential integrity

### Validation Rules

- `title`: Must be between 1 and 200 characters (inclusive)
- `description`: Optional, but if provided must be ≤ 1000 characters
- `completed`: Boolean value (True/False), defaults to False
- `user_id`: Must reference an existing user in the system
- `created_at`: Auto-populated on record creation
- `updated_at`: Auto-populated on record creation and any subsequent updates

### Indexes

1. **Primary Index**: `id` (auto-created by primary key)
2. **User Access Index**: `user_id` (for efficient user-specific queries)
3. **Status Filtering Index**: `completed` (for efficient completion status filtering)
4. **Composite Index**: `(user_id, completed)` (for efficient user-specific status queries)

### State Transitions

- **Creation**: `completed = False`, `created_at = now()`, `updated_at = now()`
- **Update**: `updated_at = now()` (whenever any field is modified)
- **Completion**: `completed = True`, `updated_at = now()`
- **Deletion**: Record removed (cascaded when user is deleted)

### Access Patterns

1. **View All Tasks**: Query by `user_id`
2. **Filter Completed**: Query by `user_id` AND `completed = True`
3. **Filter Pending**: Query by `user_id` AND `completed = False`
4. **Single Task Access**: Query by `user_id` AND `id`
5. **Create Task**: Insert with `user_id`, `title`, optional `description`
6. **Update Task**: Update by `user_id` AND `id`
7. **Delete Task**: Remove by `user_id` AND `id`