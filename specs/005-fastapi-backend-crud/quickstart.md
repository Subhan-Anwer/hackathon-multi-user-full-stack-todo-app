# Quickstart Guide: FastAPI Backend with CRUD Operations & JWT Security

## Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL (or Neon Serverless PostgreSQL)
- Better Auth configured in frontend

### Environment Variables
```bash
# Database configuration
DATABASE_URL=postgresql://username:password@localhost/dbname
NEON_DATABASE_URL=your_neon_connection_string

# Authentication
BETTER_AUTH_SECRET=your_jwt_secret_key
```

### Installation
```bash
# Navigate to backend directory
cd backend/

# Install dependencies
pip install -r requirements.txt

# Start the development server
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

### Base URL: `http://localhost:8000`

All endpoints require:
- JWT token in Authorization header: `Bearer <token>`
- User ID in URL path: `/api/{user_id}/...`

### Available Endpoints

#### `GET /api/{user_id}/tasks`
Retrieve all tasks for a specific user
- **Headers**: `Authorization: Bearer <token>`
- **Response**: Array of task objects

#### `POST /api/{user_id}/tasks`
Create a new task
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{ "title": "Task title", "description": "Optional description" }`
- **Response**: Created task object

#### `GET /api/{user_id}/tasks/{id}`
Get a specific task
- **Headers**: `Authorization: Bearer <token>`
- **Response**: Task object

#### `PUT /api/{user_id}/tasks/{id}`
Update a task
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{ "title": "New title", "description": "New description", "completed": false }`
- **Response**: Updated task object

#### `DELETE /api/{user_id}/tasks/{id}`
Delete a task
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "message": "Task deleted successfully" }`

#### `PATCH /api/{user_id}/tasks/{id}/complete`
Toggle task completion status
- **Headers**: `Authorization: Bearer <token>`
- **Response**: Updated task object with toggled completion status

## Authentication Flow

1. User authenticates via Better Auth on frontend
2. Better Auth creates JWT token stored in httpOnly cookie
3. Frontend attaches JWT to backend requests
4. Backend verifies JWT and extracts user_id
5. Backend compares extracted user_id with URL user_id parameter
6. Backend filters database queries by authenticated user_id

## Testing the API

```bash
# Example request with JWT
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     http://localhost:8000/api/user123/tasks
```

## Database Models

### Task Model
- `id`: Primary key, auto-incrementing integer
- `title`: Required string (max 255 chars)
- `description`: Optional string (max 1000 chars)
- `completed`: Boolean, default false
- `user_id`: String, links to authenticated user
- `created_at`: Timestamp
- `updated_at`: Timestamp (updates on modification)