"""FastMCP server entry point for the Figma integration.

Run with:
    uv run server.py
"""

from mcp.server.fastmcp import FastMCP

from tools import register_tools

mcp = FastMCP("figma")

# Register all Figma tools onto the server instance.
register_tools(mcp)

if __name__ == "__main__":
    mcp.run()
