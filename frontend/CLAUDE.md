# Frontend Guidelines - Next.js 16+ Todo App

## ⚠️ CRITICAL: Directory Structure

**ALL SOURCE CODE MUST BE IN `src/` DIRECTORY**
- ✅ Correct: `frontend/src/app/page.tsx`
- ✅ Correct: `frontend/src/components/ui/button.tsx`
- ❌ Wrong: `frontend/app/page.tsx` (do not use)
- ❌ Wrong: `frontend/components/ui/button.tsx` (do not use)

See `/PROJECT_STRUCTURE.md` for complete details.

## Project Context

This is the frontend layer of a multi-user todo application built with Next.js 16+ using the App Router. It integrates with Better Auth for authentication and communicates with a FastAPI backend via JWT tokens.

## Tech Stack

- **Framework:** Next.js 16+ (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Authentication:** Better Auth with JWT tokens
- **UI Components:** shadcn/ui (component library)
- **HTTP Client:** Fetch API with custom wrapper
- **State Management:** React hooks + Server Components

## Project Structure

```
frontend/
├── src/
│   ├── app/              # App Router pages and layouts
│   │   ├── layout.tsx    # Root layout with providers
│   │   ├── page.tsx      # Home page
│   │   ├── login/        # Login page
│   │   ├── signup/       # Signup page
│   │   └── dashboard/    # Protected dashboard
│   ├── components/       # Reusable UI components
│   │   ├── ui/          # shadcn/ui base components
│   │   ├── auth/        # Auth-related components
│   │   └── tasks/       # Task-related components
│   ├── lib/             # Utility functions and shared logic
│   │   ├── api.ts       # API client for backend communication
│   │   ├── auth.ts      # Better Auth configuration
│   │   └── utils.ts     # General utilities
│   ├── hooks/           # Custom React hooks
│   ├── types/           # TypeScript type definitions
│   └── styles/          # Global styles (if needed)
├── public/              # Static assets
├── .env.local           # Environment variables
└── CLAUDE.md           # This file
```

## Core Principles

### 1. Server Components by Default
- Use React Server Components (RSC) by default for better performance
- Only add `"use client"` directive when you need:
  - Browser APIs (localStorage, window, document)
  - Event handlers (onClick, onChange, onSubmit)
  - React hooks (useState, useEffect, useContext)
  - Third-party libraries that require client-side rendering

### 2. Authentication Flow

**Better Auth + JWT Integration:**
```typescript
// Better Auth is configured to issue JWT tokens
// Tokens are stored in httpOnly cookies for security
// Every API request includes the JWT token automatically
```

**Protected Routes Pattern:**
```typescript
// app/dashboard/page.tsx
import { auth } from '@/lib/auth'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const session = await auth()

  if (!session?.user) {
    redirect('/login')
  }

  return <div>Protected content</div>
}
```

### 3. API Communication

**All backend calls must use the API client:**

```typescript
// lib/api.ts structure
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = {
  // Tasks
  getTasks: async (userId: string) => { /* ... */ },
  createTask: async (userId: string, data: CreateTaskInput) => { /* ... */ },
  updateTask: async (userId: string, taskId: number, data: UpdateTaskInput) => { /* ... */ },
  deleteTask: async (userId: string, taskId: number) => { /* ... */ },
  toggleComplete: async (userId: string, taskId: number) => { /* ... */ },
}
```

**Usage in components:**
```typescript
import { api } from '@/lib/api'

// In Server Component
const tasks = await api.getTasks(session.user.id)

// In Client Component
const handleCreate = async (data: CreateTaskInput) => {
  try {
    const newTask = await api.createTask(userId, data)
    // Update UI
  } catch (error) {
    // Handle error
  }
}
```

### 4. JWT Token Handling

**Automatic Token Attachment:**
```typescript
// API client automatically includes JWT from httpOnly cookies
// Browser sends cookies with every request to same-origin or configured CORS

async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const response = await fetch(url, {
    ...options,
    credentials: 'include', // Include httpOnly cookies
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })

  if (response.status === 401) {
    // Token expired or invalid - redirect to login
    window.location.href = '/login'
    throw new Error('Unauthorized')
  }

  return response
}
```

## Component Patterns

### Client Components (with "use client")

```typescript
'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'

export function TaskForm({ onSubmit }: TaskFormProps) {
  const [title, setTitle] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      await onSubmit({ title })
      setTitle('')
    } catch (error) {
      console.error('Failed to create task:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Task title"
      />
      <Button type="submit" disabled={isLoading}>
        {isLoading ? 'Creating...' : 'Create Task'}
      </Button>
    </form>
  )
}
```

### Server Components

```typescript
// app/dashboard/page.tsx
import { auth } from '@/lib/auth'
import { api } from '@/lib/api'
import { TaskList } from '@/components/tasks/task-list'

export default async function DashboardPage() {
  const session = await auth()
  const tasks = await api.getTasks(session.user.id)

  return (
    <div>
      <h1>My Tasks</h1>
      <TaskList tasks={tasks} userId={session.user.id} />
    </div>
  )
}
```

## Styling Guidelines

### Tailwind CSS Best Practices

```typescript
// ✅ Good: Use Tailwind utility classes
<div className="flex items-center gap-4 p-4 rounded-lg border border-gray-200">
  <h2 className="text-lg font-semibold">Task Title</h2>
</div>

// ❌ Bad: Inline styles
<div style={{ display: 'flex', padding: '16px' }}>
  <h2 style={{ fontSize: '18px' }}>Task Title</h2>
</div>

// ✅ Good: Use cn() utility for conditional classes
import { cn } from '@/lib/utils'

<div className={cn(
  "p-4 rounded-lg border",
  isCompleted && "bg-green-50 border-green-200",
  isSelected && "ring-2 ring-blue-500"
)}>
```

### Component Styling Pattern

```typescript
// Use shadcn/ui components as base
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader } from '@/components/ui/card'

// Extend with Tailwind for custom styling
<Card className="max-w-md mx-auto">
  <CardHeader>
    <h2 className="text-xl font-bold">Task Details</h2>
  </CardHeader>
  <CardContent>
    <p className="text-gray-600">Task description...</p>
  </CardContent>
</Card>
```

## Error Handling

### API Error Handling Pattern

```typescript
import { toast } from 'sonner' // or your toast library

async function handleTaskCreate(data: CreateTaskInput) {
  try {
    const task = await api.createTask(userId, data)
    toast.success('Task created successfully')
    return task
  } catch (error) {
    if (error instanceof Error) {
      // Known error with message
      toast.error(error.message)
    } else {
      // Unknown error
      toast.error('Failed to create task. Please try again.')
    }
    throw error
  }
}
```

### Form Validation

```typescript
import { z } from 'zod'

const taskSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200, 'Title too long'),
  description: z.string().max(1000, 'Description too long').optional(),
})

type TaskInput = z.infer<typeof taskSchema>

function validateTask(data: unknown): TaskInput {
  return taskSchema.parse(data)
}
```

## TypeScript Best Practices

### Type Definitions

```typescript
// types/task.ts
export interface Task {
  id: number
  user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

export interface CreateTaskInput {
  title: string
  description?: string
}

export interface UpdateTaskInput {
  title?: string
  description?: string
  completed?: boolean
}
```

### Prop Types

```typescript
// ✅ Good: Explicit prop types
interface TaskCardProps {
  task: Task
  onUpdate: (id: number, data: UpdateTaskInput) => Promise<void>
  onDelete: (id: number) => Promise<void>
}

export function TaskCard({ task, onUpdate, onDelete }: TaskCardProps) {
  // ...
}

// ❌ Bad: Any types
function TaskCard(props: any) { }
```

## Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
```

**Important:**
- Prefix client-side variables with `NEXT_PUBLIC_`
- Never expose sensitive secrets on client side
- Use the same `BETTER_AUTH_SECRET` in both frontend and backend

## File Naming Conventions

```
✅ Good:
- task-list.tsx (component files)
- use-tasks.ts (custom hooks)
- api.ts (utilities)
- task.ts (types)

❌ Bad:
- TaskList.tsx
- useTasks.ts
- API.ts
```

## Code Organization Rules

### 1. Colocation
Place components close to where they're used:
```
app/
├── dashboard/
│   ├── page.tsx
│   ├── task-form.tsx      # Only used in dashboard
│   └── task-stats.tsx     # Only used in dashboard
├── components/
│   └── tasks/
│       └── task-card.tsx  # Used across multiple pages
```

### 2. Barrel Exports
Use index.ts for clean imports:
```typescript
// components/tasks/index.ts
export { TaskCard } from './task-card'
export { TaskList } from './task-list'
export { TaskForm } from './task-form'

// Usage
import { TaskCard, TaskList, TaskForm } from '@/components/tasks'
```

### 3. Separation of Concerns
```typescript
// ✅ Good: Separate data fetching from UI
// app/dashboard/page.tsx
async function DashboardPage() {
  const tasks = await getTasks()
  return <TaskList tasks={tasks} />
}

// ❌ Bad: Mix data fetching and UI
function DashboardPage() {
  const [tasks, setTasks] = useState([])
  useEffect(() => { fetchTasks() }, [])
  return <div>{tasks.map(...)}</div>
}
```

## Performance Guidelines

### 1. Use React Suspense
```typescript
import { Suspense } from 'react'

export default function Page() {
  return (
    <Suspense fallback={<TaskListSkeleton />}>
      <TaskList />
    </Suspense>
  )
}
```

### 2. Optimize Images
```typescript
import Image from 'next/image'

<Image
  src="/avatar.png"
  alt="User avatar"
  width={40}
  height={40}
  priority // For above-fold images
/>
```

### 3. Code Splitting
```typescript
// Lazy load heavy components
import dynamic from 'next/dynamic'

const TaskEditor = dynamic(() => import('@/components/tasks/task-editor'), {
  loading: () => <p>Loading editor...</p>,
})
```

## Security Best Practices

### 1. XSS Prevention
```typescript
// ✅ Good: React escapes by default
<div>{task.title}</div>

// ❌ Bad: dangerouslySetInnerHTML without sanitization
<div dangerouslySetInnerHTML={{ __html: task.description }} />

// ✅ Good: If HTML needed, sanitize first
import DOMPurify from 'isomorphic-dompurify'
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(task.description) }} />
```

### 2. CSRF Protection
```typescript
// Better Auth handles CSRF tokens automatically with httpOnly cookies
// No additional CSRF token management needed
```

### 3. Input Validation
```typescript
// Always validate on both client and server
// Client-side for UX, server-side for security
const taskSchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().max(1000).optional(),
})

// Validate before sending to API
const validatedData = taskSchema.parse(formData)
```

## Testing Guidelines

### Component Testing
```typescript
// task-card.test.tsx
import { render, screen } from '@testing-library/react'
import { TaskCard } from './task-card'

describe('TaskCard', () => {
  it('renders task title', () => {
    const task = { id: 1, title: 'Test Task', completed: false }
    render(<TaskCard task={task} />)
    expect(screen.getByText('Test Task')).toBeInTheDocument()
  })
})
```

## Common Patterns

### Loading States
```typescript
'use client'

export function TaskList() {
  const [isLoading, setIsLoading] = useState(true)

  if (isLoading) {
    return <TaskListSkeleton />
  }

  return <div>{/* tasks */}</div>
}
```

### Optimistic Updates
```typescript
async function handleToggleComplete(taskId: number) {
  // Optimistically update UI
  setTasks(tasks.map(t =>
    t.id === taskId ? { ...t, completed: !t.completed } : t
  ))

  try {
    await api.toggleComplete(userId, taskId)
  } catch (error) {
    // Revert on error
    setTasks(tasks)
    toast.error('Failed to update task')
  }
}
```

## Development Commands

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint

# Run type check
npm run type-check
```

## Debugging Tips

### 1. React DevTools
- Install React DevTools browser extension
- Inspect component props and state
- Profile performance

### 2. Network Tab
- Monitor API requests/responses
- Check JWT tokens in request headers
- Verify CORS configuration

### 3. Console Logging
```typescript
// Use structured logging
console.log('Task created:', { taskId, userId, timestamp: Date.now() })

// Remove before committing
// Use environment check for debug logs
if (process.env.NODE_ENV === 'development') {
  console.debug('Debug info:', data)
}
```

## Referencing Specs

When implementing features, always reference the relevant specification:
- `@specs/features/task-crud.md` - Task CRUD operations
- `@specs/features/authentication.md` - Authentication flow
- `@specs/api/rest-endpoints.md` - API endpoint contracts
- `@specs/ui/components.md` - UI component specifications

## Key Reminders

1. ✅ **Server Components by default** - Only use client components when necessary
2. ✅ **Use the API client** - Never call fetch directly to backend
3. ✅ **JWT via httpOnly cookies** - Tokens handled automatically, use `credentials: 'include'`
4. ✅ **Type everything** - Full TypeScript coverage, no `any` types
5. ✅ **Tailwind only** - No inline styles, use utility classes
6. ✅ **User isolation** - All API calls include userId, backend enforces isolation
7. ✅ **Error handling** - Try/catch all API calls, show user-friendly messages
8. ✅ **Validate inputs** - Use Zod schemas for form validation
9. ✅ **Follow conventions** - kebab-case files, explicit prop types, barrel exports
10. ✅ **Test coverage** - Write tests for critical user flows

## Questions or Issues?

- Check `@specs/` for feature specifications
- Review `/CLAUDE.md` for project-wide guidelines
- Consult Next.js 16 documentation for App Router patterns
- Reference Better Auth documentation for authentication details
