# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `001-ai-chatbot` | **Date**: 2026-01-31 | **Spec**: [specs/001-ai-chatbot/spec.md](spec.md)
**Input**: Feature specification from `/specs/001-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a floating AI-powered chatbot for the existing todo application that allows users to manage tasks through natural language commands. The solution includes a frontend chat interface with floating icon, backend API for chat processing, OpenAI agent integration with MCP tools for task operations, and proper data isolation for user privacy.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript 5.x (frontend), Next.js 16+
**Primary Dependencies**: FastAPI (backend), Next.js App Router (frontend), SQLModel ORM, OpenAI Agents SDK, Better Auth, Tailwind CSS
**Storage**: Neon Serverless PostgreSQL database with conversation/message tables
**Testing**: pytest (backend), Jest/Vitest (frontend)
**Target Platform**: Web application (browser-based)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <5 second response time for AI queries, 95% success rate for natural language commands
**Constraints**: Must maintain existing Phase 2 functionality, proper user data isolation, JWT authentication enforcement
**Scale/Scope**: Individual user task management, single-tenant data model

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Spec-Driven Development: Following feature spec in `/specs/001-ai-chatbot/spec.md`
- ✅ Monorepo Structure: Extending existing codebase without changing structure
- ✅ Technology Stack Compliance: Using Next.js 16+, FastAPI, SQLModel, Tailwind CSS, OpenAI Agents SDK
- ✅ Security and Authentication: Requiring JWT authentication for all chat endpoints, enforcing user_id isolation
- ✅ API Design: Adding POST /api/chat endpoint while maintaining existing task endpoints
- ✅ Database Rules: Adding conversations and messages tables as specified, with proper indexing
- ✅ Frontend Patterns: Implementing chat interface component alongside existing UI
- ✅ Interactive Chatbot Requirements: Ensuring fully functional UI with enabled inputs and clickable buttons
- ✅ Floating Chatbot UI Design: Implementing floating icon with fixed positioning and proper panel behavior
- ✅ Real-Time Interaction Design: Professional UI with message distinction and smooth animations
- ✅ AI Integration Principles: Using OpenAI Agents SDK with MCP tools for task operations
- ✅ MCP Tools Integration: Implementing standardized interfaces for task operations
- ✅ Data Privacy and Ethics: Enforcing user data isolation and privacy

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── conversation.py      # Conversation entity model
│   │   └── message.py           # Message entity model
│   ├── services/
│   │   ├── chat_service.py      # Core chat processing logic
│   │   └── mcp_tools.py         # MCP tools for task operations
│   ├── api/
│   │   └── routes/
│   │       └── chat.py          # Chat API endpoints
│   └── agents/
│       └── todo_agent.py        # OpenAI agent for todo operations
└── tests/

frontend/
├── src/
│   ├── components/
│   │   └── ChatBot.tsx          # Main chatbot component with floating UI
│   ├── lib/
│   │   └── api.ts               # API client with JWT handling
│   └── app/
│       └── dashboard/
│           └── page.tsx         # Dashboard page with chat integration
└── tests/
```

**Structure Decision**: Web application with separate backend and frontend directories following existing project architecture. Backend implements new chat API endpoints and AI agent functionality, while frontend adds the floating chatbot UI component that can be integrated across authenticated pages.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | | |
