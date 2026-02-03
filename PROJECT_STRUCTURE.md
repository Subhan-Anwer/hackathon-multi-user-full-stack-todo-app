# Definitive Project Structure

**Last Updated**: 2026-02-03
**Purpose**: Single source of truth for directory organization

## ✅ VERIFIED ACTUAL STRUCTURE

```
hackathon-multi-user-full-stack-todo-app/
│
├── .claude/                    # Claude Code configuration
├── .git/                       # Git repository
├── .specify/                   # Spec-Kit Plus framework
│   ├── memory/
│   │   └── constitution.md
│   ├── templates/
│   └── scripts/
│
├── specs/                      # Specifications (Spec-Kit Plus)
│   ├── 001-project-foundation/ # Current feature
│   │   ├── spec.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── research.md
│   │   ├── data-model.md
│   │   ├── quickstart.md
│   │   ├── contracts/
│   │   └── checklists/
│   ├── features/               # Feature specs (empty, for future)
│   ├── api/                    # API specs (empty, for future)
│   ├── database/               # Database specs (empty, for future)
│   └── ui/                     # UI specs (empty, for future)
│
├── history/                    # Prompt History & Decisions
│   ├── prompts/
│   │   ├── 001-project-foundation/
│   │   ├── constitution/
│   │   └── general/
│   └── adr/                    # Architecture Decision Records
│
├── frontend/                   # Next.js 16 Application
│   ├── src/                    # ⚠️ SOURCE ROOT (Next.js uses src/)
│   │   ├── app/                # Next.js App Router
│   │   │   ├── (auth)/         # Route group for auth pages
│   │   │   ├── (dashboard)/    # Route group for protected pages
│   │   │   ├── api/            # API routes (server-side)
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   └── globals.css
│   │   ├── components/         # React components
│   │   │   ├── ui/             # Reusable UI components
│   │   │   └── features/       # Feature-specific components
│   │   └── lib/                # Utilities and helpers
│   │       └── utils.ts
│   ├── public/                 # Static assets
│   ├── node_modules/           # Dependencies (gitignored)
│   ├── .next/                  # Build output (gitignored)
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── postcss.config.mjs
│   ├── eslint.config.mjs
│   ├── components.json
│   ├── .gitignore
│   ├── CLAUDE.md               # Frontend-specific guidelines
│   └── README.md
│
├── backend/                    # FastAPI Application
│   ├── app/                    # ⚠️ APPLICATION ROOT (Python uses app/)
│   │   ├── main.py             # FastAPI entry point
│   │   ├── models/             # SQLModel database models
│   │   │   └── __init__.py
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   │   └── __init__.py
│   │   ├── routes/             # API route handlers
│   │   │   └── __init__.py
│   │   ├── middleware/         # Custom middleware
│   │   │   └── __init__.py
│   │   ├── dependencies/       # FastAPI dependencies
│   │   │   └── __init__.py
│   │   └── utils/              # Utility functions
│   │       └── __init__.py
│   ├── .venv/                  # Virtual environment (gitignored)
│   ├── pyproject.toml          # UV package manager config
│   ├── .python-version         # Python version (3.12+)
│   ├── .env                    # Environment variables (gitignored)
│   ├── CLAUDE.md               # Backend-specific guidelines
│   └── README.md
│
├── .env                        # Root environment variables (gitignored)
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore patterns
├── docker-compose.yml          # Service orchestration (to be created)
├── CLAUDE.md                   # Root agent instructions
├── README.md                   # Project documentation (to be created)
└── PROJECT_STRUCTURE.md        # This file
```

## 🚨 CRITICAL RULES

### Frontend (Next.js 16)

**✅ CORRECT PATHS:**
- Source code: `frontend/src/app/`
- Components: `frontend/src/components/{ui,features}/`
- Utilities: `frontend/src/lib/`
- Static files: `frontend/public/`

**❌ INCORRECT PATHS (DO NOT USE):**
- ~~`frontend/app/`~~ (empty, not used)
- ~~`frontend/components/`~~ (empty, not used)
- ~~`frontend/lib/`~~ (empty, not used)

**Why src/ directory?**
- Next.js 16 convention: Separates source from config
- All TypeScript/React code lives under `src/`
- Config files (next.config.ts, package.json) stay at root

### Backend (FastAPI + UV)

**✅ CORRECT PATHS:**
- Application code: `backend/app/`
- Models: `backend/app/models/`
- Routes: `backend/app/routes/`
- Middleware: `backend/app/middleware/`
- Schemas: `backend/app/schemas/`
- Dependencies: `backend/app/dependencies/`
- Utils: `backend/app/utils/`

**❌ INCORRECT PATHS (DO NOT CREATE):**
- ~~`backend/routes/`~~ (wrong - should be under app/)
- ~~`backend/models/`~~ (wrong - should be under app/)
- ~~`backend/middleware/`~~ (wrong - should be under app/)
- ~~`backend/services/`~~ (wrong - should be under app/)

**Why app/ directory?**
- FastAPI convention: Separates app from config
- All Python code lives under `app/`
- Config files (pyproject.toml, .python-version) stay at root
- Follows Python packaging standards

## 📝 Path Reference Quick Guide

### When Creating New Files

**Frontend Components:**
```bash
# ✅ Correct
frontend/src/components/ui/button.tsx
frontend/src/components/features/task-list.tsx

# ❌ Wrong
frontend/components/ui/button.tsx
```

**Frontend Pages:**
```bash
# ✅ Correct
frontend/src/app/tasks/page.tsx
frontend/src/app/(auth)/login/page.tsx

# ❌ Wrong
frontend/app/tasks/page.tsx
```

**Backend Routes:**
```bash
# ✅ Correct
backend/app/routes/tasks.py
backend/app/routes/auth.py

# ❌ Wrong
backend/routes/tasks.py
```

**Backend Models:**
```bash
# ✅ Correct
backend/app/models/task.py
backend/app/models/user.py

# ❌ Wrong
backend/models/task.py
```

## 🔧 Import Statements

### Frontend (TypeScript)

**From components:**
```typescript
// ✅ Correct
import { Button } from '@/components/ui/button'
import { TaskList } from '@/components/features/task-list'
import { cn } from '@/lib/utils'

// ❌ Wrong
import { Button } from '../components/ui/button'
```

**tsconfig.json should have:**
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### Backend (Python)

**From app modules:**
```python
# ✅ Correct
from app.models.task import Task
from app.routes import tasks
from app.middleware.auth import JWTMiddleware

# ❌ Wrong
from models.task import Task
from routes import tasks
```

**When running:**
```bash
# ✅ Correct
uvicorn app.main:app --reload

# ❌ Wrong
uvicorn main:app --reload
```

## 📦 Package Manager Details

### Frontend: npm
- Lock file: `package-lock.json`
- Commands: `npm install`, `npm run dev`
- Dependencies in: `frontend/node_modules/`

### Backend: uv
- Config: `pyproject.toml`
- Commands: `uv sync`, `uv run <command>`
- Virtual env: `backend/.venv/`
- Python version: `backend/.python-version` (3.12+)

## 🔍 Verification Commands

**Check frontend structure:**
```bash
ls -la frontend/src/app/
ls -la frontend/src/components/
```

**Check backend structure:**
```bash
ls -la backend/app/
ls -la backend/app/models/
```

**Verify no duplicate directories:**
```bash
# These should NOT exist:
ls frontend/app/ 2>/dev/null && echo "❌ Remove frontend/app/" || echo "✅ OK"
ls backend/routes/ 2>/dev/null && echo "❌ Remove backend/routes/" || echo "✅ OK"
```

## 📋 Checklist for New Contributors

- [ ] Frontend source code goes in `frontend/src/`
- [ ] Backend application code goes in `backend/app/`
- [ ] Never create `frontend/{app,components,lib}` at root
- [ ] Never create `backend/{routes,models,middleware}` at root
- [ ] Use `@/` imports in frontend TypeScript
- [ ] Use `app.` imports in backend Python
- [ ] Verify structure with commands above

## 🔄 Migration Notes

**If you see old structure references:**
- Update `frontend/app/` → `frontend/src/app/`
- Update `backend/routes/` → `backend/app/routes/`
- Check CLAUDE.md files are updated
- Check tasks.md references are corrected

## ⚠️ Common Mistakes to Avoid

1. **Creating duplicate directories** at wrong levels
2. **Mixing src/ and root-level** frontend code
3. **Putting backend code outside app/**
4. **Wrong import paths** in code
5. **Incorrect working directory** when running commands

---

**This document is the source of truth. When in doubt, refer here.**
