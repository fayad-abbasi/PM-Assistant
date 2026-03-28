"""Miro MCP server entry point.

Run with:
    uv run --directory mcp-servers/miro-server python server.py
"""

from mcp.server.fastmcp import FastMCP

from tools import (
    add_sticky_notes,
    add_user_journey,
    create_board,
    create_mind_map,
    export_board_link,
)

mcp = FastMCP(
    "PM Assistant — Miro",
    description=(
        "Miro integration for the PM Assistant. "
        "Create boards, affinity maps, mind maps, and visual journey maps."
    ),
)

# -- Register tools -----------------------------------------------------------

mcp.tool()(create_board)
mcp.tool()(add_sticky_notes)
mcp.tool()(create_mind_map)
mcp.tool()(add_user_journey)
mcp.tool()(export_board_link)

# -- Main ---------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
