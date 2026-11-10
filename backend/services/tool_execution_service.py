
import ipaddress
from typing import Any

from jsonschema import ValidationError, validate

from backend.services.tool_registry import get_tool


class ToolExecutionError(RuntimeError):
    """Raised when a tool cannot be safely executed."""


def execute_tool(
    tool_id: str,
    arguments: dict[str, Any],
    allowed_tool_ids: list[str],
) -> dict[str, Any]:
    """Validate permissions and execute a registered simulated tool."""

    # 1. Check agent permissions.
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

    # 3. Only IP Reputation is implemented currently.
    if tool_id != "ip_reputation":
        raise ToolExecutionError(
            f"Tool '{tool_id}' is not implemented yet."
        )

    # 4. Validate arguments against the registry schema.
    try:
        validate(
            instance=arguments,
            schema=tool["input_schema"],
        )
    except ValidationError as exc:
        raise ToolExecutionError(
            f"Invalid arguments for '{tool_id}': {exc.message}"
        ) from exc

    # 5. Perform additional IP-specific validation.
    try:
        validated_ip = ipaddress.ip_address(
            arguments["ip_address"]
        )
    except ValueError as exc:
        raise ToolExecutionError(
            "A valid IPv4 or IPv6 address is required."
        ) from exc

    # 6. Generate deterministic simulated output.
    result = {
        "ip_address": str(validated_ip),
        "risk_level": "low",
        "score": 10,
    }

    # 7. Validate output against the registry contract.
    try:
        validate(
            instance=result,
            schema=tool["output_schema"],
        )
    except ValidationError as exc:
        raise ToolExecutionError(
            f"Tool '{tool_id}' returned invalid output: {exc.message}"
        ) from exc

    return result
