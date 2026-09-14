"use client";

import Link from "next/link";
import { useCallback } from "react";
import {
  addEdge,
  useEdgesState,
  useNodesState,
  type Connection,
  type Edge,
  type Node,
} from "@xyflow/react";

import WorkflowCanvas from "@/components/workflow/WorkflowCanvas";

const initialNodes: Node[] = [];
const initialEdges: Edge[] = [];

export default function NewWorkflowPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (connection: Connection) => {
      setEdges((currentEdges) => addEdge(connection, currentEdges));
    },
    [setEdges]
  );

  const addWorkflowNode = (type: string, label: string) => {
  const newNode: Node = {
    id: `${type}-${Date.now()}`,
    type: "workflowNode",
    position: {
      x: 100 + nodes.length * 40,
      y: 100 + nodes.length * 40,
    },
    data: {
      label,
      description: `Configure your ${label.toLowerCase()} node`,
      nodeType: type,
    },
  };

  setNodes((currentNodes) => [...currentNodes, newNode]);
};

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <header className="border-b border-slate-800 px-6 py-6">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <div>
            <Link
              href="/"
              className="text-sm text-sky-400 hover:text-sky-300"
            >
              ← Back to Dashboard
            </Link>

            <h1 className="mt-3 text-2xl font-bold">
              Create New Workflow
            </h1>
          </div>

          <button className="rounded-lg bg-sky-500 px-5 py-3 font-medium text-slate-950 hover:bg-sky-400">
            Save Workflow
          </button>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl grid-cols-[220px_1fr] gap-5 p-6">
        <aside className="rounded-xl border border-slate-800 bg-slate-900 p-4">
          <h2 className="font-semibold">Node Palette</h2>

          <div className="mt-4 space-y-3">
            <button
              onClick={() => addWorkflowNode("trigger", "Trigger")}
              className="w-full rounded-lg border border-slate-700 px-3 py-3 text-left hover:bg-slate-800"
            >
              Trigger
            </button>

            <button
              onClick={() => addWorkflowNode("agent", "AI Agent")}
              className="w-full rounded-lg border border-slate-700 px-3 py-3 text-left hover:bg-slate-800"
            >
              AI Agent
            </button>

            <button
              onClick={() => addWorkflowNode("condition", "Condition")}
              className="w-full rounded-lg border border-slate-700 px-3 py-3 text-left hover:bg-slate-800"
            >
              Condition
            </button>

            <button
              onClick={() => addWorkflowNode("action", "Action")}
              className="w-full rounded-lg border border-slate-700 px-3 py-3 text-left hover:bg-slate-800"
            >
              Action
            </button>
          </div>
        </aside>

        <section className="h-[650px] rounded-xl border border-slate-800 bg-slate-900 p-4">
          <div className="mb-4">
            <h2 className="font-semibold">Workflow Canvas</h2>
            <p className="text-sm text-slate-400">
              Add nodes and connect them to design your workflow.
            </p>
          </div>

          <div className="h-[570px]">
            <WorkflowCanvas
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
            />
          </div>
        </section>
      </div>
    </main>
  );
}