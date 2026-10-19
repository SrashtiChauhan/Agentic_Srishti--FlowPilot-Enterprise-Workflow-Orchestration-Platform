"""Central registry of FlowPilot's initial simulated tools.

These definitions describe available tools and their contracts.
They do not execute real SIEM, AWS, or Slack operations.
"""

from copy import deepcopy
from typing import Any


_TOOL_REGISTRY: dict[str, dict[str, Any]] = {
    "siem_search": {
        "id": "siem_search",
        "name": "SIEM Search",
        "description": "Simulate searching security event logs.",
        "category": "security",
        "mode": "simulated",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search expression for security events.",
                },
                "time_range": {
                    "type": "string",
                    "description": "Time window to search, such as 1h or 24h.",
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "events": {"type": "array", "items": {"type": "object"}},
                "total": {"type": "integer"},
            },
            "required": ["events", "total"],
            "additionalProperties": False,
        },
    },
    "ip_reputation": {
        "id": "ip_reputation",
        "name": "IP Reputation",
        "description": "Simulate checking an IP address's threat reputation.",
        "category": "security",
        "mode": "simulated",
        "input_schema": {
            "type": "object",
            "properties": {
                "ip_address": {
                    "type": "string",
                    "description": "IPv4 or IPv6 address to investigate.",
                },
            },
            "required": ["ip_address"],
            "additionalProperties": False,
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "ip_address": {"type": "string"},
                "risk_level": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "unknown"],
                },
                "score": {"type": "integer", "minimum": 0, "maximum": 100},
            },
            "required": ["ip_address", "risk_level", "score"],
            "additionalProperties": False,
        },
    },
    "aws_api": {
        "id": "aws_api",
        "name": "AWS API",
        "description": "Describe a simulated AWS operation; no cloud changes are made.",
        "category": "cloud",
        "mode": "simulated",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["inspect_resource", "quarantine_resource"],
                },
                "resource_id": {
                    "type": "string",
                    "description": "Identifier of the resource to inspect.",
                },
            },
            "required": ["operation", "resource_id"],
            "additionalProperties": False,
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "operation": {"type": "string"},
                "resource_id": {"type": "string"},
                "status": {
                    "type": "string",
                    "enum": ["simulated", "requires_approval"],
                },
                "message": {"type": "string"},
            },
            "required": ["operation", "resource_id", "status", "message"],
            "additionalProperties": False,
        },
    },
    "slack_api": {
        "id": "slack_api",
        "name": "Slack API",
        "description": "Preview a simulated Slack notification without sending it.",
        "category": "communication",
        "mode": "simulated",
        "input_schema": {
            "type": "object",
            "properties": {
                "channel": {
                    "type": "string",
                    "description": "Destination channel name or identifier.",
                },
                "message": {
                    "type": "string",
                    "description": "Notification text.",
                },
            },
            "required": ["channel", "message"],
            "additionalProperties": False,
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "channel": {"type": "string"},
                "status": {"type": "string", "enum": ["preview_only"]},
                "message": {"type": "string"},
            },
            "required": ["channel", "status", "message"],
            "additionalProperties": False,
        },
    },
}


def list_tools() -> list[dict[str, Any]]:
    """Return all registered tools without exposing mutable registry data."""
    return [deepcopy(tool) for tool in _TOOL_REGISTRY.values()]


def get_tool(tool_id: str) -> dict[str, Any] | None:
    """Return one tool definition, or None if the ID is not registered."""
    tool = _TOOL_REGISTRY.get(tool_id)
    return deepcopy(tool) if tool is not None else None


def validate_tool_ids(tool_ids: list[str]) -> list[str]:
    """Return IDs that are not present in the registry."""
    return sorted(set(tool_ids) - _TOOL_REGISTRY.keys())
