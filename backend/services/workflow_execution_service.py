from typing import Any

from backend.services.workflow_engine import (
    WorkflowValidationError,
    get_execution_order,
)


def prepare_workflow_execution(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Validate a workflow and return its nodes in execution order.
    """
    execution_order = get_execution_order(nodes, edges)

    nodes_by_id = {
        node["id"]: node
        for node in nodes
    }

    return [
        nodes_by_id[node_id]
        for node_id in execution_order
    ]