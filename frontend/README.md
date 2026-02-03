# Frontend - Next.js 16+ Todo Application

This is the frontend application for the multi-user todo app, built with Next.js 16+ App Router, TypeScript, and Tailwind CSS.

## Tech Stack

- **Framework**: Next.js 16.1.6 (App Router)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 4
- **UI Components**: Radix UI, shadcn/ui
- **Authentication**: Better Auth with JWT tokens
- **HTTP Client**: Fetch API with custom wrapper

## Prerequisites

- Node.js 20+ and npm
- Backend API running (see `../backend/README.md`)

## Getting Started

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Create `.env.local` file:

```bash
# Copy from example (if exists) or create manually
cp .env.local.example .env.local

# Or create with required variables
cat > .env.local << 'EOF'
BETTER_AUTH_SECRET=your-secret-key-at-least-32-characters-long
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
EOF
```

**⚠️ CRITICAL**: `BETTER_AUTH_SECRET` must match the backend secret exactly.

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Available Scripts

```bash
# Development server with hot reload
npm run dev

# Build for production
npm run build

# Start production server (requires build first)
npm start

# Run ESLint
npm run lint

# Type checking (if configured)
npm run type-check
```

## Project Structure

```
frontend/
├── src/
│   ├── app/              # App Router pages and layouts
│   │   ├── page.tsx      # Home page
│   │   ├── layout.tsx    # Root layout
│   │   ├── login/        # Login page
│   │   ├── signup/       # Signup page
│   │   └── dashboard/    # Protected dashboard
│   ├── components/       # Reusable components
│   │   ├── ui/          # Base UI components (shadcn/ui)
│   │   ├── auth/        # Auth-related components
│   │   └── tasks/       # Task components
│   ├── lib/             # Utilities
│   │   ├── api.ts       # API client
│   │   ├── auth.ts      # Better Auth config
│   │   └── utils.ts     # Helper functions
│   └── types/           # TypeScript types
├── public/              # Static assets
└── CLAUDE.md            # Development guidelines
```

**⚠️ IMPORTANT**: All source code must be in `src/` directory:
- ✅ Correct: `src/app/page.tsx`
- ❌ Wrong: `app/page.tsx`

## Development Guidelines

### Server Components by Default

Use React Server Components by default. Only add `"use client"` when you need:
- Browser APIs (localStorage, window)
- Event handlers (onClick, onChange)
- React hooks (useState, useEffect)

### API Communication

All API calls should use the client in `src/lib/api.ts`:

```typescript
import { api } from '@/lib/api'

// In Server Component
const tasks = await api.getTasks(userId)

// In Client Component
const handleCreate = async (data) => {
  const task = await api.createTask(userId, data)
}
```

### Styling with Tailwind

Use Tailwind utility classes:

```typescript
<div className="flex items-center gap-4 p-4 rounded-lg border">
  <h2 className="text-lg font-semibold">Task Title</h2>
</div>
```

### Type Safety

Always use TypeScript types:

```typescript
interface Task {
  id: number
  user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}
```

## Authentication

This app uses Better Auth with JWT tokens stored in httpOnly cookies:

1. User logs in → JWT token created
2. Token stored in httpOnly cookie (secure, not accessible via JavaScript)
3. Browser automatically sends cookie with requests
4. Backend verifies token and extracts user_id

## Common Issues

### Port Already in Use

```bash
# Kill process on port 3000
lsof -i :3000
kill -9 <PID>
```

### Environment Variables Not Loading

- Ensure `.env.local` exists in `frontend/` directory
- Restart dev server after changing `.env.local`
- Use `NEXT_PUBLIC_` prefix for client-side variables

### Module Not Found

```bash
# Clear Next.js cache
rm -rf .next
npm install
npm run dev
```

### TypeScript Errors

```bash
# Rebuild TypeScript definitions
rm -rf .next
npm run dev
```

## Code Quality

- Follow guidelines in `CLAUDE.md`
- Use TypeScript for all new code
- Run linter before committing
- Write tests for new features (when applicable)

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Next.js 16 App Router](https://nextjs.org/docs/app)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Better Auth](https://www.better-auth.com/docs)
- [Radix UI](https://www.radix-ui.com/)

## Additional Documentation

- See `/CLAUDE.md` for project-wide guidelines
- See `CLAUDE.md` (this directory) for frontend-specific patterns
- See `/specs/` for feature specifications
- See `/README.md` for complete project setup

---

**Questions?** Check the root `README.md` or `CLAUDE.md` files.
