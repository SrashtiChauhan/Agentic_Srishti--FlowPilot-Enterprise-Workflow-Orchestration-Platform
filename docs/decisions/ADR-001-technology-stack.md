# ADR-001: FlowPilot Technology Stac

* **Status:** Accepted
* **Date:** 2026-09-12
* **Decision Type:** Architecture
* **Project:** FlowPilot — Enterprise Workflow Orchestration Platform

## Context

FlowPilot is a workflow orchestration platform that combines visual workflow design, AI agents, human-in-the-loop approvals, asynchronous execution, telemetry, and external integrations.

The existing architecture documentation allows multiple implementation technologies. This ADR records the initial technology choices for the production-quality MVP.

The goal is to select technologies that:

* Support the documented architecture.
* Are practical for a beginner to learn incrementally.
* Have mature ecosystems.
* Support asynchronous execution.
* Provide reliable AI and database integrations.
* Can be deployed within the planned two-month MVP timeline.

## Decisions

### 1. Frontend — Next.js with React and TypeScript

**Selected technology:** Next.js + React + TypeScript

**Why:**

* Supports modern React application development.
* Provides routing and application structure.
* TypeScript improves type safety.
* Supports production deployment.
* Has a large ecosystem and strong community support.

**Alternatives considered:**

* React with Vite
* Vue
* Angular

**Reason for not selecting them initially:**

React with Vite is a valid alternative, but Next.js provides a more complete application structure for this project. Vue and Angular are also capable, but React aligns better with the selected React Flow ecosystem.

---

### 2. Workflow Canvas — React Flow

**Selected technology:** React Flow

**Why:**

* Designed specifically for node-based editors.
* Supports draggable nodes and edges.
* Supports custom node components.
* Supports graph interactions and viewport controls.
* Reduces the need to manually implement canvas mechanics.

The architecture documentation describes custom SVG and Bezier connections. React Flow will provide the interaction layer while allowing custom styling and rendering where required.

**Alternatives considered:**

* Custom SVG canvas
* HTML Canvas API
* D3.js

**Reason for not selecting them initially:**

A custom canvas would require implementing dragging, selection, connection handling, zooming, and viewport management manually. React Flow provides these capabilities while allowing FlowPilot-specific node behavior.

---

### 3. Frontend State Management — Zustand

**Selected technology:** Zustand

**Why:**

* Lightweight.
* Simple API.
* Suitable for workflow nodes, edges, and editor state.
* Less boilerplate than larger state-management libraries.

**Alternatives considered:**

* React Context
* Redux Toolkit
* Jotai

**Reason for not selecting them initially:**

React Context is useful for simple global state but can become inconvenient for complex workflow editor state. Redux Toolkit is powerful but introduces more structure than needed for the initial MVP.

---

### 4. Backend API — FastAPI

**Selected technology:** Python FastAPI

**Why:**

* Supports asynchronous Python applications.
* Provides automatic API documentation.
* Uses Pydantic for validation.
* Integrates naturally with AI and data-processing libraries.
* Works well with LangGraph and multiple AI provider SDKs.

**Alternatives considered:**

* Node.js with Express
* Node.js with NestJS
* Django REST Framework

**Reason for not selecting them initially:**

Node.js is a valid choice and remains an option for future services. FastAPI is preferred because FlowPilot's core backend includes AI orchestration, asynchronous execution, structured validation, and Python-based AI libraries.

---

### 5. AI Agent Orchestration — LangGraph

**Selected technology:** LangGraph

**Why:**

* Represents agent workflows using nodes and edges.
* Supports stateful execution.
* Supports conditional transitions.
* Supports human-in-the-loop patterns.
* Supports tool calling and multi-step agent behavior.

**Important architectural boundary:**

LangGraph will not replace the entire FlowPilot visual workflow engine.

The architecture will be:

```text
FlowPilot Workflow Engine
        |
        v
     Agent Node
        |
        v
   LangGraph Runtime
        |
        v
 AI Provider + Tools + Agent State
```

FlowPilot controls the business workflow. LangGraph controls reasoning inside an Agent node.

**Alternatives considered:**

* LangChain only
* AutoGen
* Custom agent runtime

**Reason for not selecting them initially:**

LangChain is useful as a library layer but does not provide the same graph-oriented execution model by itself. AutoGen is useful for multi-agent conversations but would add complexity before the core workflow engine is stable.

---

### 6. LLM Provider — Provider-Agnostic Free/Open Model Strategy

**Selected technology:** Provider adapter with Mistral API, Hugging Face Inference API, and Ollama fallback.

**Why:**

* Avoids mandatory dependency on paid LLM APIs.
* Supports development within free-tier and open-source constraints.
* Allows the project to use Mistral or other open models available through Hugging Face.
* Ollama provides a local fallback when API quotas are unavailable or exceeded.
* Keeps the application flexible if model availability or pricing changes.

**Implementation approach:**

The backend will communicate with an abstract AI provider interface instead of directly calling a specific LLM provider.

```text
FastAPI
   |
   v
AI Provider Interface
   |
   +--> MistralProvider
   |
   +--> HuggingFaceProvider
   |
   +--> OllamaProvider
```

The provider interface will expose common operations such as:

* Text generation.
* Structured JSON generation.
* Tool-calling support where available.

All AI-generated workflow definitions must be validated using Pydantic schemas before they are accepted by the workflow engine.

**Original architecture note:**

The initial architecture documentation specified Google Gemini API. For the MVP implementation, Gemini will not be a required dependency because its free tier has usage limits and paid usage may be required at scale. Gemini may be added later as another provider without changing the workflow engine.

**Alternatives considered:**

* Google Gemini API.
* OpenAI API.
* Anthropic API.
* Local open-source models only.

**Reason for not selecting Gemini initially:**

Gemini is technically suitable, but making it the primary dependency could introduce cost and quota constraints. A provider-agnostic design provides greater flexibility for a free MVP.

**Reason for not selecting local-only models:**

Running models locally can require significant RAM, storage, and processing power. API-based free/open providers are easier for initial development, while Ollama remains available as a fallback.
---

### 7. Database — PostgreSQL

**Selected technology:** PostgreSQL

**Why:**

FlowPilot contains strongly related data:

```text
Users
  → Workspaces
  → Workflows
  → Workflow Versions
  → Nodes and Edges
  → Executions
  → Logs
  → Approvals
```

PostgreSQL provides:

* Relational integrity.
* Transactions.
* Structured queries.
* Reliable persistence for workflow execution.
* Suitable support for audit and approval records.

**Alternatives considered:**

* MongoDB
* SQLite

**Reason for not selecting them initially:**

MongoDB is useful for flexible document storage, but FlowPilot's execution, approval, and audit data have strong relationships. SQLite is useful for local experiments but is not the primary production database target.

---

### 8. ORM and Migrations — SQLAlchemy and Alembic

**Selected technologies:** SQLAlchemy + Alembic

**Why:**

* SQLAlchemy provides database access and ORM support.
* Alembic manages database schema migrations.
* Both are mature Python ecosystem tools.

**Alternative considered:**

* SQLModel

**Reason for not selecting it initially:**

SQLModel is a good alternative and may be reconsidered if it simplifies the learning experience. SQLAlchemy is selected for its maturity and widespread production usage.

---

### 9. Queue and Cache — Redis

**Selected technology:** Redis

**Why:**

Redis will initially support:

* Asynchronous task coordination.
* Queue infrastructure.
* Temporary execution state where appropriate.
* Rate limiting and future caching.

Redis is already aligned with the documented asynchronous execution architecture.

---

### 10. Background Worker — ARQ

**Selected technology:** ARQ

**Why:**

* Built for Python asyncio.
* Integrates naturally with FastAPI-style asynchronous applications.
* Uses Redis.
* Simpler initial setup than Celery.

**Alternative considered:**

* Celery

**Reason for not selecting it initially:**

Celery is mature and remains a possible future choice. ARQ is preferred for the MVP because the project is designed around asynchronous Python execution and requires a simpler worker architecture during initial development.

This is an implementation refinement, not a change to the architectural requirement for Redis-based asynchronous workers.

---

### 11. Real-Time Updates — Server-Sent Events

**Selected technology:** Server-Sent Events (SSE)

**Why:**

FlowPilot primarily needs server-to-client updates for:

* Workflow execution status.
* Node status changes.
* Execution logs.
* Approval events.
* Telemetry updates.

SSE is suitable because the initial communication pattern is mostly one-way: the backend sends live updates to the frontend.

**Alternative considered:**

* WebSockets

**Reason for not selecting it initially:**

WebSockets are useful for bidirectional real-time communication. SSE is simpler for the initial telemetry and execution-monitoring requirements.

---

### 12. Styling — Tailwind CSS

**Selected technology:** Tailwind CSS

**Why:**

* Supports rapid UI development.
* Provides utility-based styling.
* Makes responsive design easier.
* Fits the documented cyber-glassmorphic interface direction.

The design system will use dark slate surfaces with cyan, amber, rose, emerald, and purple accents.

---

### 13. Testing

**Selected tools:**

* Vitest
* React Testing Library
* Pytest

**Why:**

These tools provide coverage for:

* Frontend components.
* State-management behavior.
* Backend services.
* API endpoints.
* Workflow execution logic.

Testing will be introduced alongside features instead of being postponed until the end.

---

## Consequences

### Positive Consequences

* The stack supports the AI-focused nature of FlowPilot.
* The frontend and backend remain modular.
* PostgreSQL provides reliable relational persistence.
* React Flow accelerates visual editor development.
* FastAPI and LangGraph align naturally with Python-based AI development.
* Redis and ARQ support asynchronous workflow execution.
* The stack can be deployed incrementally.- The application must handle provider-specific differences in structured output and tool calling.
- Free API quotas may require rate limiting and a local fallback.


### Trade-offs

* Two languages must be maintained: TypeScript and Python.
* FastAPI and Next.js require separate development environments.
* Redis introduces an additional infrastructure dependency.
* LangGraph and FlowPilot require a clear separation of responsibilities.
* React Flow reduces canvas implementation effort but requires learning its API.

## Rejected Alternatives

The following technologies are not permanently rejected. They are simply not part of the initial MVP stack:

* Express as the primary backend.
* MongoDB as the primary database.
* Celery as the initial worker.
* AutoGen as the primary orchestration framework.
* A custom SVG workflow canvas.
* WebSockets for the initial telemetry channel.

They may be evaluated later if project requirements change.

## Review Conditions

This ADR should be revisited if:

* Workflow execution requires distributed scheduling beyond the MVP.
* Agent orchestration becomes significantly more complex.
* Real-time communication becomes bidirectional.
* Database performance or scale requirements change.
* Deployment constraints require a different architecture.
