export type WorkflowStatus = "Draft" | "Active" | "Paused";

export interface Workflow {
  id: string;
  name: string;
  description?: string;
  status: WorkflowStatus;
  updatedAt: string;
}

export type WorkflowNodeType =
  | "trigger"
  | "agent"
  | "condition"
  | "hitl"
  | "action"
  | "webhook";

export type WorkflowNodeStatus =
  | "idle"
  | "running"
  | "completed"
  | "failed"
  | "waiting_approval";

export interface WorkflowNodeConfig {
  agentId?: string;
  triggerType?: "webhook" | "schedule" | "event" | "manual";
  actionType?: "slack" | "jira" | "email" | "database" | "github" | "api";
  conditionLogic?: string;
  prompt?: string;
  temperature?: number;
  riskScore?: "low" | "medium" | "high" | "critical";
  requireApprovalRole?: string;
}

export interface WorkflowNode {
  id: string;
  type: WorkflowNodeType;
  title: string;
  subtitle?: string;
  icon?: string;

  position: {
    x: number;
    y: number;
  };

  status: WorkflowNodeStatus;

  config: WorkflowNodeConfig;
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
}