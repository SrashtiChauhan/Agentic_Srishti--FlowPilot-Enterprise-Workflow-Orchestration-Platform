"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import {
  addEdge,
  useEdgesState,
  useNodesState,
  type Connection,
  type Edge,
  type Node,
  type NodeMouseHandler,
  type ReactFlowInstance,
} from "@xyflow/react";

import WorkflowCanvas from "@/components/workflow/WorkflowCanvas";
import NodeInspector from "@/components/workflow/NodeInspector";
import { useWorkflowStore } from "@/store/workflowStore";
import type { WorkflowNodeType } from "@/types/workflow";

const initialNodes: Node[] = [];
const initialEdges: Edge[] = [];

export default function NewWorkflowPage() {
  const updateNodeInStore = useWorkflowStore((state) => state.updateNode);
  const addNodeToStore = useWorkflowStore((state) => state.addNode);
  const setEdgesInStore = useWorkflowStore((state) => state.setEdges);
  const removeNodeFromStore = useWorkflowStore((state) => state.removeNode);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [isSaved, setIsSaved] = useState(false);
  const [reactFlowInstance, setReactFlowInstance] =
  useState<ReactFlowInstance | null>(null);
  useEffect(() => {
    const savedWorkflow = localStorage.getItem("flowpilot-workflow-draft");

    if (!savedWorkflow) {
      return;
    }

    try {
      const workflowGraph = JSON.parse(savedWorkflow);

      if (
        Array.isArray(workflowGraph.nodes) &&
        Array.isArray(workflowGraph.edges)
      ) {
        setNodes(workflowGraph.nodes);
        setEdges(workflowGraph.edges);

        useWorkflowStore.getState().setNodes(workflowGraph.nodes);
        useWorkflowStore.getState().setEdges(workflowGraph.edges);

        console.log("Workflow loaded locally:", workflowGraph);
      }
    } catch (error) {
      console.error("Failed to load saved workflow:", error);
    }
  }, [setNodes, setEdges]);

  const onNodeClick: NodeMouseHandler = useCallback((_event, node) => {
    setSelectedNode(node);
    console.log("Selected node:", node);
  }, []);

  const onNodesChangeWithStore = useCallback(
    (changes: Parameters<typeof onNodesChange>[0]) => {
      onNodesChange(changes);

      changes.forEach((change) => {
        if (change.type === "remove") {
          removeNodeFromStore(change.id);
        }

        if (change.type === "position" && change.position) {
          updateNodeInStore(change.id, {
            position: {
              x: change.position.x,
              y: change.position.y,
            },
          });
        }
      });
    },
    [onNodesChange, removeNodeFromStore, updateNodeInStore],
  );

  const updateNode = useCallback(
    (nodeId: string, updates: Record<string, unknown>) => {
      updateNodeInStore(nodeId, updates);
      setNodes((currentNodes) =>
        currentNodes.map((node) =>
          node.id === nodeId
            ? {
                ...node,
                data: {
                  ...node.data,
                  ...updates,
                },
              }
            : node,
        ),
      );

      setSelectedNode((currentNode) =>
        currentNode && currentNode.id === nodeId
          ? {
              ...currentNode,
              data: {
                ...currentNode.data,
                ...updates,
              },
            }
          : currentNode,
      );
    },
    [setNodes, updateNodeInStore],
  );

  const onConnect = useCallback(
    (connection: Connection) => {
      setEdges((currentEdges) => {
        const updatedEdges = addEdge(connection, currentEdges);

        setEdgesInStore(
          updatedEdges.map((edge) => ({
            id: edge.id,
            source: edge.source,
            target: edge.target,
          })),
        );

        return updatedEdges;
      });
    },
    [setEdges, setEdgesInStore],
  );
  const onEdgesChangeWithStore = useCallback(
    (changes: Parameters<typeof onEdgesChange>[0]) => {
      onEdgesChange(changes);

      const removedEdgeIds = new Set(
        changes
          .filter((change) => change.type === "remove")
          .map((change) => change.id),
      );

      if (removedEdgeIds.size > 0) {
        setEdgesInStore(
          edges
            .filter((edge) => !removedEdgeIds.has(edge.id))
            .map((edge) => ({
              id: edge.id,
              source: edge.source,
              target: edge.target,
            })),
        );
      }
    },
    [edges, onEdgesChange, setEdgesInStore],
  );

  const saveWorkflow = () => {
    const workflowGraph = {
      nodes,
      edges,
    };

    localStorage.setItem(
      "flowpilot-workflow-draft",
      JSON.stringify(workflowGraph),
    );

    console.log("Workflow saved locally:", workflowGraph);

    setIsSaved(true);

    setTimeout(() => {
      setIsSaved(false);
    }, 2000);
  };

  const addWorkflowNode = (type: WorkflowNodeType, title: string) => {
  if (!reactFlowInstance) {
    return;
  }

  const position = reactFlowInstance.screenToFlowPosition({
    x: window.innerWidth / 2 - 110,
    y: window.innerHeight / 2 - 70,
  });

  const newNode: Node = {
    id: `${type}-${Date.now()}`,
    type: "workflowNode",
    position,
    data: {
      title,
      subtitle: `Configure your ${title.toLowerCase()} node`,
      type,
      status: "idle",
      config: {},
    },
  };

  addNodeToStore({
    id: newNode.id,
    type,
    title,
    subtitle: `Configure your ${title.toLowerCase()} node`,
    position: newNode.position,
    status: "idle",
    config: {},
  });

  setNodes((currentNodes) => [...currentNodes, newNode]);
};

  return (
    <main className="flex h-screen flex-col overflow-hidden bg-slate-950 text-white">
      {/* Header */}
      <header className="flex h-20 shrink-0 items-center justify-between border-b border-slate-800 bg-slate-950 px-6">
        <div>
          <Link
            href="/"
            className="text-sm text-cyan-400 transition hover:text-cyan-300"
          >
            ← Back to Dashboard
          </Link>

          <h1 className="mt-1 text-lg font-extrabold tracking-tight text-white">
            Create New Workflow
          </h1>
        </div>

        <button
          onClick={saveWorkflow}
          className="rounded-lg bg-cyan-500 px-5 py-2.5 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
        >
          {isSaved ? "Saved ✓" : "Save Workflow"}
        </button>
      </header>

      {/* Main Workflow Workspace */}
      <div className="flex min-h-0 flex-1">
        {/* Node Sidebar */}
        <aside className="w-64 shrink-0 border-r border-slate-800 bg-slate-900/80 p-5 backdrop-blur-md">
          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Node Palette
            </p>

            <p className="mt-2 text-xs text-slate-500">
              Add components to build your workflow.
            </p>
          </div>

          <div className="mt-6 space-y-3">
            <button
              onClick={() => addWorkflowNode("trigger", "Trigger")}
              className="w-full rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-left text-sm font-medium transition hover:border-amber-400/50 hover:bg-slate-800"
            >
              <span className="text-amber-400">●</span>
              <span className="ml-3">Trigger</span>
            </button>

            <button
              onClick={() => addWorkflowNode("agent", "AI Agent")}
              className="w-full rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-left text-sm font-medium transition hover:border-cyan-400/50 hover:bg-slate-800"
            >
              <span className="text-cyan-400">●</span>
              <span className="ml-3">AI Agent</span>
            </button>

            <button
              onClick={() => addWorkflowNode("condition", "Condition")}
              className="w-full rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-left text-sm font-medium transition hover:border-purple-400/50 hover:bg-slate-800"
            >
              <span className="text-purple-400">●</span>
              <span className="ml-3">Condition</span>
            </button>

            <button
              onClick={() => addWorkflowNode("hitl", "Approval Request")}
              className="w-full rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-left text-sm font-medium transition hover:border-rose-400/50 hover:bg-slate-800"
            >
              <span className="text-rose-400">●</span>
              <span className="ml-3">HITL Approval</span>
            </button>

            <button
              onClick={() => addWorkflowNode("action", "Action")}
              className="w-full rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-left text-sm font-medium transition hover:border-emerald-400/50 hover:bg-slate-800"
            >
              <span className="text-emerald-400">●</span>
              <span className="ml-3">Action</span>
            </button>
          </div>
        </aside>

        {/* Full Canvas */}
        <section className="relative min-w-0 flex-1">
          <WorkflowCanvas
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChangeWithStore}
            onEdgesChange={onEdgesChangeWithStore}
            onConnect={onConnect}
            onNodeClick={onNodeClick}
            onInit={setReactFlowInstance}
          />

          {/* Canvas information */}
          <div className="pointer-events-none absolute left-5 top-4 z-10">
            <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Workflow Canvas
            </p>

            <p className="mt-1 text-xs text-slate-500">
              {nodes.length} nodes · {edges.length} connections
            </p>
          </div>
        </section>
        <NodeInspector node={selectedNode} onUpdateNode={updateNode} />
      </div>
    </main>
  );
}
