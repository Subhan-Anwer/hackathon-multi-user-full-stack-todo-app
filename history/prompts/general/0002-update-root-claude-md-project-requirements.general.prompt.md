---
id: 0002
title: Update Root CLAUDE.md with Project Requirements
stage: general
date: 2026-02-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /clear
labels: ["documentation", "project-setup", "configuration", "monorepo"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - CLAUDE.md
tests:
  - none
---

## Prompt

update the root @CLAUDE.md after reading the @project-requirement.md

## Response snapshot

Updated the root CLAUDE.md file to incorporate Phase II project requirements. Changes include:

1. **Project Context Section** - Added Phase II Todo Full-Stack Web Application context with tech stack details (Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth)

2. **API Endpoints Section** - Documented all 6 REST API endpoints with user_id path parameter structure

3. **Authentication & Security Section** - Detailed JWT token flow from Better Auth to FastAPI, including:
   - 5-step authentication flow
   - Security requirements (user isolation, shared secret, token validation)
   - Enforcement of task ownership

4. **Spec-Kit Plus Integration** - Added specification organization structure showing how specs are organized under features/, api/, database/, and ui/ folders

5. **Project Structure Section** - Completely updated to reflect actual monorepo structure with:
   - Frontend and backend folders with their own CLAUDE.md files
   - Spec-Kit Plus artifacts organization
   - Docker compose setup

6. **Development Workflow** - Added 5-step workflow from reading specs to iteration

7. **Commands Section** - Added commands for running frontend (npm), backend (uvicorn), and both (docker-compose)

8. **Code Standards** - Added project-specific standards including TypeScript, type hints, JSON responses, Pydantic models, and user isolation enforcement

## Outcome

- ✅ Impact: Root CLAUDE.md now provides comprehensive project-specific guidance aligned with Phase II requirements
- 🧪 Tests: No tests required for documentation update
- 📁 Files: Modified CLAUDE.md (3 edits applied successfully)
- 🔁 Next prompts: Create frontend/CLAUDE.md and backend/CLAUDE.md with layer-specific guidelines
- 🧠 Reflection: Successfully integrated project requirements while maintaining SDD workflow structure

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (documentation update)
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Create frontend and backend CLAUDE.md files to complete monorepo documentation structure
