"""MCP tools for the Figma server.

Each tool is a thin wrapper around FigmaClient that formats the response
for consumption by Claude Code slash commands (especially /ux).
"""

from __future__ import annotations

import os
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP

from figma_client import FigmaClient, FigmaAPIError

# Reference to the shared MCP server instance (created in server.py,
# but we need the decorator here). We import it at registration time.
mcp: FastMCP | None = None


def register_tools(server: FastMCP) -> None:
    """Register all Figma tools on the given MCP server."""

    global mcp  # noqa: PLW0603
    mcp = server

    # ------------------------------------------------------------------
    # get_file
    # ------------------------------------------------------------------
    @mcp.tool()
    async def get_file(file_key: str) -> dict:
        """Get Figma file metadata and structure (pages, frames, components).

        Parameters
        ----------
        file_key : str
            The key from a Figma file URL, e.g. the `abc123` part of
            https://www.figma.com/file/abc123/My-Design.
        """
        try:
            async with FigmaClient() as client:
                data = await client.get_file(file_key)
        except FigmaAPIError as exc:
            return {"error": exc.detail, "status_code": exc.status_code}

        # Extract a lightweight summary instead of returning the full tree.
        document = data.get("document", {})
        pages = []
        components = data.get("components", {})

        for page in document.get("children", []):
            frames = [
                {"id": child.get("id"), "name": child.get("name"), "type": child.get("type")}
                for child in page.get("children", [])
            ]
            pages.append({
                "id": page.get("id"),
                "name": page.get("name"),
                "frames": frames,
            })

        return {
            "name": data.get("name"),
            "last_modified": data.get("lastModified"),
            "version": data.get("version"),
            "pages": pages,
            "component_count": len(components),
            "components": {
                cid: {"name": cdata.get("name"), "description": cdata.get("description", "")}
                for cid, cdata in components.items()
            },
        }

    # ------------------------------------------------------------------
    # get_comments
    # ------------------------------------------------------------------
    @mcp.tool()
    async def get_comments(file_key: str) -> list[dict]:
        """Read design review comments from a Figma file.

        Returns a list of comments with author, content, timestamp,
        and position information.
        """
        try:
            async with FigmaClient() as client:
                comments = await client.get_comments(file_key)
        except FigmaAPIError as exc:
            return [{"error": exc.detail, "status_code": exc.status_code}]

        return [
            {
                "id": c.get("id"),
                "author": c.get("user", {}).get("handle", "unknown"),
                "message": c.get("message", ""),
                "created_at": c.get("created_at"),
                "resolved_at": c.get("resolved_at"),
                "order_id": c.get("order_id"),
            }
            for c in comments
        ]

    # ------------------------------------------------------------------
    # get_component
    # ------------------------------------------------------------------
    @mcp.tool()
    async def get_component(file_key: str, node_id: str) -> dict:
        """Get specific component details (properties, styles, constraints).

        Parameters
        ----------
        file_key : str
            Figma file key.
        node_id : str
            The node ID of the component, e.g. "1:23".
        """
        try:
            async with FigmaClient() as client:
                data = await client.get_file_nodes(file_key, [node_id])
        except FigmaAPIError as exc:
            return {"error": exc.detail, "status_code": exc.status_code}

        nodes = data.get("nodes", {})
        node_data = nodes.get(node_id)
        if not node_data:
            return {"error": f"Node {node_id} not found in file {file_key}."}

        doc = node_data.get("document", {})
        return {
            "id": doc.get("id"),
            "name": doc.get("name"),
            "type": doc.get("type"),
            "visible": doc.get("visible", True),
            "constraints": doc.get("constraints"),
            "bounding_box": doc.get("absoluteBoundingBox"),
            "fills": doc.get("fills"),
            "strokes": doc.get("strokes"),
            "effects": doc.get("effects"),
            "styles": node_data.get("styles"),
            "children_count": len(doc.get("children", [])),
            "component_properties": doc.get("componentProperties"),
        }

    # ------------------------------------------------------------------
    # export_assets
    # ------------------------------------------------------------------
    @mcp.tool()
    async def export_assets(
        file_key: str,
        node_ids: list[str],
        format: str = "png",
    ) -> dict:
        """Export frames/components as images. Returns download URLs.

        Optionally downloads the exported images to data/ux/assets/
        if the directory exists.

        Parameters
        ----------
        file_key : str
            Figma file key.
        node_ids : list[str]
            List of node IDs to export.
        format : str
            Image format: "png", "jpg", "svg", or "pdf". Default "png".
        """
        if format not in ("png", "jpg", "svg", "pdf"):
            return {"error": f"Unsupported format '{format}'. Use png, jpg, svg, or pdf."}

        try:
            async with FigmaClient() as client:
                images = await client.get_images(file_key, node_ids, format=format)
        except FigmaAPIError as exc:
            return {"error": exc.detail, "status_code": exc.status_code}

        # Attempt to download images to data/ux/assets/ if the dir exists.
        assets_dir = _find_assets_dir()
        downloaded: dict[str, str] = {}

        if assets_dir:
            async with httpx.AsyncClient(timeout=30.0) as http:
                for node_id, url in images.items():
                    if not url:
                        continue
                    try:
                        resp = await http.get(url)
                        if resp.is_success:
                            safe_name = node_id.replace(":", "-")
                            filename = f"{file_key}_{safe_name}.{format}"
                            filepath = assets_dir / filename
                            filepath.write_bytes(resp.content)
                            downloaded[node_id] = str(filepath)
                    except Exception:
                        pass  # Download is best-effort; URLs still returned.

        return {
            "image_urls": images,
            "downloaded": downloaded if downloaded else None,
            "format": format,
        }

    # ------------------------------------------------------------------
    # post_comment
    # ------------------------------------------------------------------
    @mcp.tool()
    async def post_comment(file_key: str, message: str) -> dict:
        """Add a comment to a Figma design file.

        Parameters
        ----------
        file_key : str
            Figma file key.
        message : str
            The comment text to post.
        """
        try:
            async with FigmaClient() as client:
                result = await client.post_comment(file_key, message)
        except FigmaAPIError as exc:
            return {"error": exc.detail, "status_code": exc.status_code}

        return {
            "id": result.get("id"),
            "message": result.get("message"),
            "created_at": result.get("created_at"),
            "author": result.get("user", {}).get("handle", "unknown"),
        }


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _find_assets_dir() -> Path | None:
    """Locate the data/ux/assets/ directory relative to the project root.

    Walks up from this file's location looking for a directory that
    contains 'data/ux/assets/'. Returns None if not found.
    """
    # The server lives at mcp-servers/figma-server/, so project root
    # is two levels up.
    candidate = Path(__file__).resolve().parent.parent.parent / "data" / "ux" / "assets"
    if candidate.is_dir():
        return candidate
    # Fallback: check via env var or cwd.
    cwd_candidate = Path(os.getcwd()) / "data" / "ux" / "assets"
    if cwd_candidate.is_dir():
        return cwd_candidate
    return None
