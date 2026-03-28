"""Lucidchart MCP server entry point.

Run with:
    uv run mcp run server:mcp
"""

from mcp.server.fastmcp import FastMCP

import tools

mcp = FastMCP(
    "lucid",
    description="Lucidchart integration — create flowcharts, org charts, and architecture diagrams",
)

# Register all tools onto the server instance
tools.register(mcp)

if __name__ == "__main__":
    mcp.run()
