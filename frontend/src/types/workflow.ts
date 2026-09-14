export type WorkflowStatus = "Draft" | "Active" | "Paused";

export interface Workflow {
  id: string;
  name: string;
  description?: string;
  status: WorkflowStatus;
  updatedAt: string;
}

export interface WorkflowNode {
  id: string;
  type: string;
  label: string;
  position: {
    x: number;
    y: number;
  };
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
}