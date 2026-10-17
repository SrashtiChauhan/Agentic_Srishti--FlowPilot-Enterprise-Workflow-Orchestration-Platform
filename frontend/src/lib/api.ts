
import type { Agent, AgentInput } from "@/types/agent";

const API_BASE_URL = "http://127.0.0.1:8000";

export async function getWorkflows() {
  const response = await fetch(`${API_BASE_URL}/workflows/`);

  if (!response.ok) {
    throw new Error("Failed to fetch workflows");
  }

  return response.json();
}

export async function getWorkflow(workflowId: string) {
  const response = await fetch(
    `${API_BASE_URL}/workflows/${workflowId}`,
  );

  if (!response.ok) {
    throw new Error("Failed to fetch workflow");
  }

  return response.json();
}

export async function createWorkflow(workflow: {
  name: string;
  description?: string;
  status: "Draft" | "Active" | "Paused";
  nodes: any[];
  edges: any[];
}) {
  const response = await fetch(`${API_BASE_URL}/workflows/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: workflow.name,
      description: workflow.description,
      status: workflow.status,

      nodes: workflow.nodes.map((node) => ({
        id: node.id,
        type: node.data.type,
        title: node.data.title,
        subtitle: node.data.subtitle,
        position: {
          x: node.position.x,
          y: node.position.y,
        },
        status: node.data.status,
        config: node.data.config ?? {},
      })),

      edges: workflow.edges.map((edge) => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
      })),
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error("Create workflow API error:", errorText);

    throw new Error("Failed to create workflow");
  }

  return response.json();
}

export async function updateWorkflow(
  workflowId: string,
  workflow: {
    name: string;
    description?: string;
    status: "Draft" | "Active" | "Paused";
    nodes: any[];
    edges: any[];
  },
) {
  const response = await fetch(`${API_BASE_URL}/workflows/${workflowId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: workflow.name,
      description: workflow.description,
      status: workflow.status,

      nodes: workflow.nodes.map((node) => ({
        id: node.id,
        type: node.data.type,
        title: node.data.title,
        subtitle: node.data.subtitle,
        position: {
          x: node.position.x,
          y: node.position.y,
        },
        status: node.data.status,
        config: node.data.config ?? {},
      })),

      edges: workflow.edges.map((edge) => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
      })),
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error("Update workflow API error:", errorText);

    throw new Error("Failed to update workflow");
  }

  return response.json();
}

export async function getAgents(): Promise<{ agents: Agent[] }> {
  const response = await fetch(`${API_BASE_URL}/agents/`);

  if (!response.ok) {
    throw new Error("Failed to fetch agents");
  }

  return response.json();
}

export async function getAgent(agentId: string): Promise<Agent> {
  const response = await fetch(
    `${API_BASE_URL}/agents/${agentId}`,
  );

  if (!response.ok) {
    throw new Error("Failed to fetch agent");
  }

  return response.json();
}

export async function createAgent(
  agent: AgentInput,
): Promise<{ message: string; agent: Agent }> {
  const response = await fetch(`${API_BASE_URL}/agents/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(agent),
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error("Create agent API error:", errorText);
    throw new Error("Failed to create agent");
  }

  return response.json();
}

export async function updateAgent(
  agentId: string,
  agent: AgentInput,
): Promise<{ message: string; agent: Agent }> {
  const response = await fetch(
    `${API_BASE_URL}/agents/${agentId}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(agent),
    },
  );

  if (!response.ok) {
    const errorText = await response.text();
    console.error("Update agent API error:", errorText);
    throw new Error("Failed to update agent");
  }

  return response.json();
}

export async function deleteAgent(
  agentId: string,
): Promise<{ message: string; id: string }> {
  const response = await fetch(
    `${API_BASE_URL}/agents/${agentId}`,
    {
      method: "DELETE",
    },
  );

  if (!response.ok) {
    const errorText = await response.text();
    console.error("Delete agent API error:", errorText);
    throw new Error("Failed to delete agent");
  }

  return response.json();
}


export interface AgentRunResponse {
  agent_id: string;
  agent_name: string;
  model_name: string;
  output: string;
}

export async function runAgent(
  agentId: string,
  userInput: string,
): Promise<AgentRunResponse> {
  const response = await fetch(
    `${API_BASE_URL}/agents/${encodeURIComponent(agentId)}/run`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_input: userInput,
      }),
    },
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    const message =
      typeof errorData?.detail === "string"
        ? errorData.detail
        : "Failed to execute agent";

    throw new Error(message);
  }

  return response.json() as Promise<AgentRunResponse>;
}
