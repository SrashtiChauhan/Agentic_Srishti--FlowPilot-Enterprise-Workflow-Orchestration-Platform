
from collections import deque
from typing import Any


class WorkflowValidationError(ValueError):
    """Raised when a workflow graph is invalid."""


def get_execution_order(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> list[str]:
    """Validate a workflow graph and return its topological order."""

    node_ids: list[str] = []
    node_id_set: set[str] = set()

    for node in nodes:
        node_id = node.get("id")

        if not isinstance(node_id, str) or not node_id:
            raise WorkflowValidationError(
                "Every node must have a non-empty string ID."
            )

        if node_id in node_id_set:
            raise WorkflowValidationError(
                f"Duplicate node ID: {node_id}"
            )

        node_ids.append(node_id)
        node_id_set.add(node_id)

    adjacency: dict[str, list[str]] = {
        node_id: [] for node_id in node_ids
    }
    in_degree: dict[str, int] = {
        node_id: 0 for node_id in node_ids
    }

    seen_edges: set[tuple[str, str]] = set()

    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")

        if source not in node_id_set or target not in node_id_set:
            raise WorkflowValidationError(
                f"Edge references a missing node: {source} -> {target}"
            )

        if source == target:
            raise WorkflowValidationError(
                f"Self-connections are not allowed: {source}"
            )

        edge_pair = (source, target)

        if edge_pair in seen_edges:
            raise WorkflowValidationError(
                f"Duplicate edge: {source} -> {target}"
            )

        seen_edges.add(edge_pair)
        adjacency[source].append(target)
        in_degree[target] += 1

    # Preserve the original node order where possible.
    ready = deque(
        node_id for node_id in node_ids
        if in_degree[node_id] == 0
    )
    execution_order: list[str] = []

    while ready:
        current = ready.popleft()
        execution_order.append(current)

        for neighbor in adjacency[current]:
            in_degree[neighbor] -= 1

            if in_degree[neighbor] == 0:
                ready.append(neighbor)

    if len(execution_order) != len(node_ids):
        raise WorkflowValidationError(
            "Workflow contains a cycle and cannot be executed."
        )

    return execution_order
