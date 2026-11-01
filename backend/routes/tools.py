from fastapi import APIRouter, HTTPException

from backend.services.tool_registry import get_tool, list_tools

router = APIRouter(
    prefix="/tools",
    tags=["Tools"],
)


@router.get("/")
def get_available_tools():
    """List all registered tools and their schemas."""
    return {"tools": list_tools()}


@router.get("/{tool_id}")
def get_tool_details(tool_id: str):
    """Return details for one registered tool."""
    tool = get_tool(tool_id)

    if tool is None:
        raise HTTPException(
            status_code=404,
            detail=f"Tool '{tool_id}' not found",
        )

    return tool
