"""PyWA MCP Tools - Modular tool implementations for WhatsApp messaging."""

from .messaging import register_messaging_tools
from .interactive import register_interactive_tools
from .templates import register_template_tools

__all__ = [
    "register_messaging_tools",
    "register_interactive_tools", 
    "register_template_tools",
]


def register_all_tools(mcp, wa_client):
    """Register all available tools with the MCP server."""
    register_messaging_tools(mcp, wa_client)
    register_interactive_tools(mcp, wa_client)
    register_template_tools(mcp, wa_client)