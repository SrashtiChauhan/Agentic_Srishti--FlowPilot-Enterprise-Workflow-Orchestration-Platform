from collections import deque
from typing import Any

from sqlalchemy.orm import Session

from backend.services.agent_execution_service import (
    AgentExecutionError,
    execute_agent,
)
from backend.services.workflow_engine import (
    WorkflowValidationError,
    get_execution_order,
)


class WorkflowExecutionError(RuntimeError):
    """Raised when a workflow cannot be executed."""


def prepare_workflow_execution(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Validate a workflow and return its nodes in execution order."""

    execution_order = get_execution_order(nodes, edges)

    nodes_by_id = {
        node["id"]: node
        for node in nodes
    }

    return [
        nodes_by_id[node_id]
        for node_id in execution_order
    ]


def execute_workflow(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    db: Session,
    initial_input: str,
) -> dict[str, Any]:
    """Execute a workflow containing supported trigger and agent nodes."""

    
    try:
        ordered_nodes = prepare_workflow_execution(nodes, edges)
    except WorkflowValidationError as exc:
        raise WorkflowExecutionError(str(exc)) from exc

    if not ordered_nodes:
        raise WorkflowExecutionError(
            "Cannot execute an empty workflow."
        )

    # Validate that the workflow has exactly one trigger.
    trigger_nodes = [
        node
        for node in ordered_nodes
        if node.get("type") == "trigger"
    ]

    if len(trigger_nodes) != 1:
        raise WorkflowExecutionError(
            "A workflow must contain exactly one trigger node."
        )

    
    # Verify that every node is reachable from the trigger.
    trigger_id = trigger_nodes[0]["id"]

    adjacency: dict[str, list[str]] = {
        node["id"]: [] for node in ordered_nodes
    }

    for edge in edges:
        adjacency[edge["source"]].append(edge["target"])

    reachable = {trigger_id}
    queue = deque([trigger_id])

    while queue:
        current = queue.popleft()

        for neighbor in adjacency[current]:
            if neighbor not in reachable:
                reachable.add(neighbor)
                queue.append(neighbor)

    if len(reachable) != len(ordered_nodes):
        raise WorkflowExecutionError(
            "Workflow contains disconnected nodes."
        )


    # Keep the existing context and execution loop below this.
    context: dict[str, Any] = {
        "input": initial_input,
        "outputs": {},
    }


    for node in ordered_nodes:
        node_id = node["id"]
        node_type = node.get("type")

        if node_type == "trigger":
            context["outputs"][node_id] = {
                "status": "completed",
                "output": context["input"],
            }

        elif node_type == "agent":
            config = node.get("config") or {}
            agent_id = config.get("agentId")

            if not isinstance(agent_id, str) or not agent_id.strip():
                raise WorkflowExecutionError(
                    f"Agent node '{node_id}' has no configured agentId."
                )

            agent_input = context["input"]

            try:
                result = execute_agent(
                    agent_id=agent_id,
                    user_input=agent_input,
                    db=db,
                )
            except AgentExecutionError as exc:
                raise WorkflowExecutionError(
                    f"Agent node '{node_id}' failed: {exc}"
                ) from exc

            context["input"] = result["output"]
            context["outputs"][node_id] = {
                "status": "completed",
                "output": result["output"],
                "agent_id": result["agent_id"],
                "model_name": result["model_name"],
            }

        else:
            raise WorkflowExecutionError(
                f"Node '{node_id}' has unsupported type: {node_type!r}."
            )

    return {
        "status": "completed",
        "outputs": context["outputs"],
        "final_output": context["input"],
    }
