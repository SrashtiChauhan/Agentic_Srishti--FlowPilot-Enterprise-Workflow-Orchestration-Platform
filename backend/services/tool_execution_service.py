import ipaddress
from typing import Any

from backend.services.tool_registry import get_tool


class ToolExecutionError(RuntimeError):
    """Raised when a tool cannot be safely executed."""


def execute_tool(
    tool_id: str,
    arguments: dict[str, Any],
    allowed_tool_ids: list[str],
) -> dict[str, Any]:
    """Validate permissions and execute a registered simulated tool."""

    # 1. Check whether the agent is allowed to use this tool.
    if tool_id not in allowed_tool_ids:
        raise ToolExecutionError(
            f"Agent is not authorized to use tool '{tool_id}'."
        )

    # 2. Retrieve the registered tool definition.
    tool = get_tool(tool_id)

    if tool is None:
        raise ToolExecutionError(
            f"Tool '{tool_id}' is not registered."
        )

    # 3. Restrict this first implementation to IP Reputation.
    if tool_id != "ip_reputation":
        raise ToolExecutionError(
            f"Tool '{tool_id}' is not implemented yet."
        )

    # 4. Validate the argument structure.
    if not isinstance(arguments, dict):
        raise ToolExecutionError("Tool arguments must be an object.")

    if set(arguments.keys()) != {"ip_address"}:
        raise ToolExecutionError(
            "IP Reputation requires only the 'ip_address' argument."
        )

    ip_address = arguments["ip_address"]

    if not isinstance(ip_address, str):
        raise ToolExecutionError(
            "The IP address must be a string."
        )

    try:
        validated_ip = ipaddress.ip_address(ip_address)
    except ValueError as exc:
        raise ToolExecutionError(
            "A valid IPv4 or IPv6 address is required."
        ) from exc

    # 5. Return deterministic sample data.
    return {
        "ip_address": str(validated_ip),
        "risk_level": "low",
        "score": 10,
        "mode": "simulated",
        "message": "Sample reputation result; no external threat intelligence was queried.",
    }