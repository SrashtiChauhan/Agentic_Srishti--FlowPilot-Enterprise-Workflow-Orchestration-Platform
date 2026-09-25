import { create } from "zustand";
import type { WorkflowEdge, WorkflowNode } from "@/types/workflow";

interface WorkflowState {
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];

  setNodes: (nodes: WorkflowNode[]) => void;
  setEdges: (edges: WorkflowEdge[]) => void;
  updateNode: (nodeId: string, updates: Partial<WorkflowNode>) => void;

  addNode: (node: WorkflowNode) => void;
  removeNode: (nodeId: string) => void;
}

export const useWorkflowStore = create<WorkflowState>((set) => ({
  nodes: [],
  edges: [],

  setNodes: (nodes) => set({ nodes }),

  setEdges: (edges) => set({ edges }),
  updateNode: (nodeId, updates) =>
    set((state) => ({
      nodes: state.nodes.map((node) =>
        node.id === nodeId
          ? {
              ...node,
              ...updates,
            }
          : node,
      ),
    })),

  addNode: (node) =>
    set((state) => ({
      nodes: [...state.nodes, node],
    })),

  removeNode: (nodeId) =>
    set((state) => ({
      nodes: state.nodes.filter((node) => node.id !== nodeId),
      edges: state.edges.filter(
        (edge) => edge.source !== nodeId && edge.target !== nodeId,
      ),
    })),
}));
