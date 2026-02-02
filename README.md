# Hackathon II: Todo Full-Stack Web Application

Phase II implementation of a multi-user todo application using spec-driven development.

## 🎯 Features

- ✅ Add Task - Create new todo items
- ✅ Delete Task - Remove tasks
- ✅ Update Task - Modify task details
- ✅ View Task List - Display all tasks
- ✅ Mark as Complete - Toggle completion

## 🛠️ Tech Stack

- **Frontend:** Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend:** Python FastAPI, SQLModel ORM
- **Database:** Neon Serverless PostgreSQL
- **Authentication:** Better Auth with JWT tokens

## 📋 Prerequisites

- Node.js 18+
- Python 3.11+
- Neon PostgreSQL account
- Docker (optional)

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd hackathon-todo
cp .env.example .env
# Edit .env with your database URL and secret
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs on http://localhost:8000

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on http://localhost:3000

### 4. Using Docker (Alternative)
```bash
docker-compose up
```

## 🔒 Authentication

Users must sign up and log in to access the application. JWT tokens are stored in httpOnly cookies and automatically included in API requests via server-side proxy.

## 📚 Documentation

- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Development Guide](docs/DEVELOPMENT.md)

## 🏗️ Architecture

Frontend (Next.js) → API Proxy → Backend (FastAPI) → Database (PostgreSQL)

See [Architecture Documentation](specs/architecture.md) for details.

## 🧪 Testing
```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test

# Integration tests
./run-integration-tests.sh
```

## 📝 Development Approach

This project uses **Spec-Driven Development** with Claude Code:
1. Specifications define what to build
2. Agents implement from specs
3. Zero manual coding
4. Specifications in `/specs/` directory

## 🤝 Contributing

This is a hackathon project.