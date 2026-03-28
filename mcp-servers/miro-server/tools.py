"""MCP tools for the Miro server.

Each public function is registered as an MCP tool by ``server.py``.
"""

from __future__ import annotations

from typing import Any

from miro_client import MiroClient

# ---------------------------------------------------------------------------
# Colour palette for sticky-note clusters
# ---------------------------------------------------------------------------
STICKY_COLORS = [
    "yellow",
    "light_blue",
    "light_green",
    "light_pink",
    "orange",
    "cyan",
    "violet",
]

# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------
STICKY_SPACING_X = 280
STICKY_SPACING_Y = 300
SHAPE_SPACING_X = 320
SHAPE_SPACING_Y = 200
JOURNEY_STAGE_WIDTH = 250
JOURNEY_STAGE_HEIGHT = 120
JOURNEY_STAGE_GAP = 300


# ---------------------------------------------------------------------------
# Tool: create_board
# ---------------------------------------------------------------------------
async def create_board(name: str, description: str = "") -> dict[str, Any]:
    """Create a new Miro board.

    Args:
        name: Board name.
        description: Optional board description.

    Returns:
        ``board_id`` and ``view_link``.
    """
    async with MiroClient() as miro:
        result = await miro.create_board(name, description or None)
    return result


# ---------------------------------------------------------------------------
# Tool: add_sticky_notes
# ---------------------------------------------------------------------------
async def add_sticky_notes(
    board_id: str,
    notes: list[dict[str, Any]],
) -> dict[str, Any]:
    """Add sticky notes to a board (useful for affinity mapping from insights).

    Args:
        board_id: Target Miro board ID.
        notes: List of dicts, each with ``content`` (str) and optional
               ``color`` (str, e.g. "yellow", "light_blue").

    Returns:
        List of created item IDs and the count.
    """
    created_ids: list[str] = []
    columns = 5  # notes per row

    async with MiroClient() as miro:
        for idx, note in enumerate(notes):
            col = idx % columns
            row = idx // columns
            x = col * STICKY_SPACING_X
            y = row * STICKY_SPACING_Y
            color = note.get("color", "yellow")
            content = note.get("content", "")
            result = await miro.create_sticky_note(
                board_id, content, color=color, x=x, y=y
            )
            created_ids.append(result["item_id"])

    return {"item_ids": created_ids, "count": len(created_ids)}


# ---------------------------------------------------------------------------
# Tool: create_mind_map
# ---------------------------------------------------------------------------
async def create_mind_map(
    board_id: str,
    root: str,
    branches: list[dict[str, Any]],
) -> dict[str, Any]:
    """Create a mind-map structure using shapes and connectors.

    Args:
        board_id: Target Miro board ID.
        root: Text label for the central/root node.
        branches: List of branch dicts, each with ``label`` (str) and optional
                  ``children`` (list of dicts with ``label``).

    Returns:
        IDs for root, branch, and leaf shapes, plus connector IDs.
    """
    shape_ids: dict[str, str] = {}
    connector_ids: list[str] = []

    async with MiroClient() as miro:
        # Root node (centre)
        root_result = await miro.create_shape(
            board_id, root, shape="round_rectangle", x=0, y=0, width=260, height=120
        )
        root_id = root_result["item_id"]
        shape_ids["root"] = root_id

        # Branches radiate outward
        branch_ids: list[str] = []
        for b_idx, branch in enumerate(branches):
            bx = SHAPE_SPACING_X * (b_idx + 1)
            by = -((len(branches) - 1) * SHAPE_SPACING_Y / 2) + b_idx * SHAPE_SPACING_Y

            branch_result = await miro.create_shape(
                board_id,
                branch["label"],
                shape="round_rectangle",
                x=bx,
                y=by,
                width=220,
                height=100,
            )
            branch_id = branch_result["item_id"]
            branch_ids.append(branch_id)
            shape_ids[f"branch_{b_idx}"] = branch_id

            # Connect root -> branch
            conn = await miro.create_connector(board_id, root_id, branch_id)
            connector_ids.append(conn["connector_id"])

            # Children (leaves)
            children = branch.get("children", [])
            for c_idx, child in enumerate(children):
                cx = bx + SHAPE_SPACING_X
                cy = by - ((len(children) - 1) * SHAPE_SPACING_Y / 2) + c_idx * SHAPE_SPACING_Y

                child_result = await miro.create_shape(
                    board_id,
                    child["label"],
                    shape="rectangle",
                    x=cx,
                    y=cy,
                    width=200,
                    height=80,
                )
                child_id = child_result["item_id"]
                shape_ids[f"branch_{b_idx}_child_{c_idx}"] = child_id

                conn = await miro.create_connector(board_id, branch_id, child_id)
                connector_ids.append(conn["connector_id"])

    return {
        "shape_ids": shape_ids,
        "connector_ids": connector_ids,
    }


# ---------------------------------------------------------------------------
# Tool: add_user_journey
# ---------------------------------------------------------------------------
async def add_user_journey(
    board_id: str,
    journey_data: dict[str, Any],
) -> dict[str, Any]:
    """Create a visual user journey map on a Miro board.

    Uses shapes for stages and sticky notes for details within each stage.

    Args:
        board_id: Target Miro board ID.
        journey_data: Dict with:
            - ``title`` (str): Journey map title.
            - ``persona`` (str): Persona name.
            - ``stages`` (list[dict]): Each stage has ``name`` (str),
              ``actions`` (list[str]), ``thoughts`` (list[str]),
              ``emotions`` (list[str]), and ``pain_points`` (list[str]).

    Returns:
        IDs of created shapes and sticky notes.
    """
    stage_ids: list[str] = []
    note_ids: list[str] = []

    stages = journey_data.get("stages", [])
    title = journey_data.get("title", "User Journey")
    persona = journey_data.get("persona", "")

    async with MiroClient() as miro:
        # Title shape at the top
        await miro.create_shape(
            board_id,
            f"<strong>{title}</strong><br>Persona: {persona}",
            shape="rectangle",
            x=(len(stages) * JOURNEY_STAGE_GAP) / 2,
            y=-200,
            width=500,
            height=80,
        )

        for s_idx, stage in enumerate(stages):
            sx = s_idx * JOURNEY_STAGE_GAP

            # Stage header shape
            stage_result = await miro.create_shape(
                board_id,
                f"<strong>{stage['name']}</strong>",
                shape="rectangle",
                x=sx,
                y=0,
                width=JOURNEY_STAGE_WIDTH,
                height=JOURNEY_STAGE_HEIGHT,
            )
            stage_ids.append(stage_result["item_id"])

            # Connect stages sequentially
            if s_idx > 0:
                await miro.create_connector(
                    board_id, stage_ids[s_idx - 1], stage_ids[s_idx]
                )

            # Row offsets for each detail category
            row_config = [
                ("actions", "light_green", 180),
                ("thoughts", "light_blue", 430),
                ("emotions", "light_pink", 680),
                ("pain_points", "orange", 930),
            ]

            for field, color, base_y in row_config:
                items = stage.get(field, [])
                for i, item_text in enumerate(items):
                    result = await miro.create_sticky_note(
                        board_id,
                        item_text,
                        color=color,
                        x=sx,
                        y=base_y + i * 160,
                    )
                    note_ids.append(result["item_id"])

    return {
        "stage_ids": stage_ids,
        "note_ids": note_ids,
        "stage_count": len(stage_ids),
        "note_count": len(note_ids),
    }


# ---------------------------------------------------------------------------
# Tool: export_board_link
# ---------------------------------------------------------------------------
async def export_board_link(board_id: str) -> dict[str, str]:
    """Return the view URL for a Miro board.

    Args:
        board_id: Miro board ID.

    Returns:
        ``board_id`` and ``view_link``.
    """
    async with MiroClient() as miro:
        board = await miro.get_board(board_id)

    return {
        "board_id": board_id,
        "view_link": board.get("viewLink", f"https://miro.com/app/board/{board_id}/"),
    }
