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
