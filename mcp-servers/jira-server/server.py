"""FastMCP server entry point for the Jira integration.

Run via:  uv run python server.py
Or configured in .claude/settings.json as an MCP server.
"""

from tools import mcp

if __name__ == "__main__":
    mcp.run()
