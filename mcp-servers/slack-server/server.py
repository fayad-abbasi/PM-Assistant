"""Slack MCP server for PM Assistant.

Provides tools for searching, reading, and posting Slack messages.
Run with: uv run --directory mcp-servers/slack-server python server.py
"""

from mcp.server.fastmcp import FastMCP

from tools import (
    get_channel_history,
    get_thread,
    list_channels,
    post_message,
    search_messages,
)

mcp = FastMCP("PM Assistant Slack Server")

mcp.tool()(search_messages)
mcp.tool()(post_message)
mcp.tool()(get_channel_history)
mcp.tool()(list_channels)
mcp.tool()(get_thread)

if __name__ == "__main__":
    mcp.run()
