# FlowPilot Development Progress

## Project

**FlowPilot — Enterprise Workflow Orchestration Platform**

FlowPilot is an enterprise workflow orchestration platform combining visual workflow design, AI agents, human-in-the-loop approvals, asynchronous execution, telemetry, and external integrations.

---

# Development Status

## Current Phase

**Week 2 — Visual Workflow Builder**

**Status:** Completed

The Week 2 goal was to build a functional visual workflow editor before moving to backend persistence and execution.

---

# Week 2 — Visual Workflow Builder

## Completed Features

### 1. Workflow Canvas

Implemented the main workflow canvas using React Flow.

The canvas supports:

- Node rendering
- Node movement
- Node selection
- Edge connections
- Zoom
- Pan
- Fit view
- MiniMap
- Canvas controls

---

### 2. Node Palette

Implemented a sidebar containing workflow node types:

- Trigger
- AI Agent
- Condition
- HITL Approval
- Action

Users can add nodes directly from the palette.

---

### 3. Viewport-Aware Node Placement

Initially, nodes were placed using fixed workflow coordinates.

This caused newly created nodes to sometimes appear outside the user's currently visible canvas area.

The implementation was changed to use React Flow's:

`screenToFlowPosition()`

New nodes are now positioned relative to the currently visible canvas viewport.

### Implementation Note

This is a UX implementation detail and does not change the documented workflow architecture.

The goal is to ensure that when a user adds a node, the node appears in the visible working area rather than at an arbitrary off-screen coordinate.

---

### 4. Custom Workflow Nodes

Implemented a reusable custom workflow node component.

Each node displays:

- Node type
- Title
- Subtitle
- Status
- Input handle
- Output handle
- Type-specific visual styling

Node types use different accent colors according to the FlowPilot design direction.

---

### 5. Node Status System

Implemented support for the documented workflow node statuses:

- `idle`
- `running`
- `completed`
- `failed`
- `waiting_approval`

The node UI dynamically displays the current status.

Running and waiting-for-approval states include a subtle visual pulse.

Execution behavior itself is not implemented yet. The current implementation prepares the UI for the future workflow execution engine.

---

### 6. Node Inspector

Implemented a Node Inspector for configuring selected workflow nodes.

Common fields:

- Type
- Title
- Subtitle

Type-specific configuration includes:

#### Trigger

- Trigger Type
- Manual
- Webhook
- Schedule
- Event

#### AI Agent

- Agent ID
- Prompt
- Temperature
- Risk Score

#### Condition

- Condition Logic

#### HITL

- Required Approval Role

#### Action

- Action Type
- Slack
- Jira
- Email
- Database
- GitHub
- API

---

### 7. Node Selection

Clicking a workflow node selects it and opens its configuration in the Node Inspector.

Selection and inspector state were manually tested.

Verified behavior:

- Select node
- Edit configuration
- Click elsewhere
- Select node again
- Configuration remains synchronized

---

### 8. Workflow Connections

Implemented React Flow connections between nodes.

Users can:

- Connect nodes
- Remove connections
- Create multi-node workflow graphs

Connections are synchronized with the workflow store.

---

### 9. Node Deletion

Nodes can be deleted from the canvas.

When a node is removed, its related edges are also removed from the workflow state.

---

### 10. Zustand Workflow Store

Implemented Zustand for workflow editor state.

The store currently manages:

- Workflow nodes
- Workflow edges
- Node updates
- Node creation
- Node deletion

React Flow editor state and Zustand state are synchronized for the implemented workflow operations.

---

### 11. Local Workflow Persistence

Implemented local draft persistence using browser `localStorage`.

Storage key:

`flowpilot-workflow-draft`

The workflow graph stores:

- Nodes
- Node positions
- Node configuration
- Edges

Users can save the workflow locally and restore it after refreshing the browser.

---

# Testing Completed

The following behaviors were manually verified:

- [x] Add workflow node
- [x] Add different node types
- [x] Node appears in visible canvas area
- [x] Move node
- [x] Connect nodes
- [x] Delete node
- [x] Select node
- [x] Edit node configuration
- [x] Re-select edited node
- [x] Save workflow
- [x] Refresh browser
- [x] Restore saved workflow
- [x] Preserve node positions
- [x] Preserve connections
- [x] Preserve node configuration
- [x] Build succeeds

---

# UI / Canvas Improvements

The React Flow interface was adapted to the FlowPilot dark enterprise design.

Implemented:

- Dark React Flow color mode
- Dark canvas
- Dark MiniMap
- Canvas controls
- Workflow-specific node colors
- Dark enterprise surfaces
- Cyan, amber, purple, rose, and emerald accents

---

# Current Frontend Structure

```text
frontend/
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   ├── page.tsx
│   └── workflows/
│       └── new/
│           └── page.tsx
│
└── src/
    ├── components/
    │   └── workflow/
    │       ├── NodeInspector.tsx
    │       ├── WorkflowCanvas.tsx
    │       └── WorkflowNode.tsx
    │
    ├── store/
    │   └── workflowStore.ts
    │
    └── types/
        └── workflow.ts


### One important point

This document records **what i actually completed**, rather than claiming that backend/execution features already exist. 
