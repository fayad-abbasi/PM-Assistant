"""MCP tools for creating and managing Lucidchart diagrams.

Each tool is a thin orchestration layer: it translates PM-friendly parameters
into Lucid API calls via ``LucidClient``.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from lucid_client import LucidClient

# The FastMCP instance is created in server.py and passed here via register().
# We define a module-level reference that server.py will set.
mcp: FastMCP | None = None


def register(server: FastMCP) -> None:
    """Register all Lucid tools on the given MCP server."""

    global mcp  # noqa: PLW0603
    mcp = server

    # ------------------------------------------------------------------
    # create_flowchart
    # ------------------------------------------------------------------
    @mcp.tool()
    async def create_flowchart(
        name: str,
        nodes: list[dict],
        edges: list[dict],
    ) -> dict:
        """Create a new Lucidchart document with a flowchart.

        Args:
            name: Document title.
            nodes: List of node dicts, each with ``id``, ``label``, and
                   ``type`` (one of ``process``, ``decision``, ``start``,
                   ``end``).
            edges: List of edge dicts, each with ``from_id``, ``to_id``,
                   and optional ``label``.

        Returns:
            Dict with ``document_id``, ``edit_link``, and counts of shapes
            imported.
        """
        async with LucidClient() as client:
            doc = await client.create_document(name, product="lucidchart")
            document_id = doc["document_id"]

            # Build import payload in a format Lucid can render as shapes
            import_payload = {
                "nodes": nodes,
                "edges": edges,
            }
            await client.import_data(document_id, "json", import_payload)

            return {
                "document_id": document_id,
                "edit_link": doc["edit_link"],
                "nodes_count": len(nodes),
                "edges_count": len(edges),
            }

    # ------------------------------------------------------------------
    # create_org_chart
    # ------------------------------------------------------------------
    @mcp.tool()
    async def create_org_chart(
        name: str,
        hierarchy: dict,
    ) -> dict:
        """Create an org chart or stakeholder map in Lucidchart.

        Args:
            name: Document title.
            hierarchy: Nested dict representing the org structure. Each node
                       has ``name`` (str) and optional ``children`` (list of
                       the same shape).
                       Example::

                           {
                               "name": "CEO",
                               "children": [
                                   {"name": "VP Eng", "children": [...]},
                                   {"name": "VP Sales"}
                               ]
                           }

        Returns:
            Dict with ``document_id``, ``edit_link``, and ``node_count``.
        """

        def _flatten(node: dict, parent_id: str | None = None, counter: list | None = None) -> tuple[list[dict], list[dict]]:
            """Recursively flatten a hierarchy dict into nodes and edges."""
            if counter is None:
                counter = [0]

            node_id = f"org-{counter[0]}"
            counter[0] += 1

            nodes = [{"id": node_id, "label": node.get("name", ""), "type": "process"}]
            edges = []

            if parent_id is not None:
                edges.append({"from_id": parent_id, "to_id": node_id, "label": ""})

            for child in node.get("children", []):
                child_nodes, child_edges = _flatten(child, parent_id=node_id, counter=counter)
                nodes.extend(child_nodes)
                edges.extend(child_edges)

            return nodes, edges

        flat_nodes, flat_edges = _flatten(hierarchy)

        async with LucidClient() as client:
            doc = await client.create_document(name, product="lucidchart")
            document_id = doc["document_id"]

            import_payload = {
                "nodes": flat_nodes,
                "edges": flat_edges,
            }
            await client.import_data(document_id, "json", import_payload)

            return {
                "document_id": document_id,
                "edit_link": doc["edit_link"],
                "node_count": len(flat_nodes),
            }

    # ------------------------------------------------------------------
    # add_to_document
    # ------------------------------------------------------------------
    @mcp.tool()
    async def add_to_document(
        document_id: str,
        shapes: list[dict],
    ) -> dict:
        """Add shapes to an existing Lucidchart document.

        Args:
            document_id: The target document ID.
            shapes: List of shape dicts. Each should have at minimum
                    ``id``, ``label``, and ``type``.

        Returns:
            Dict with ``document_id`` and ``shapes_added``.
        """
        async with LucidClient() as client:
            await client.import_data(
                document_id,
                "json",
                {"nodes": shapes, "edges": []},
            )
            return {
                "document_id": document_id,
                "shapes_added": len(shapes),
            }

    # ------------------------------------------------------------------
    # get_document_link
    # ------------------------------------------------------------------
    @mcp.tool()
    async def get_document_link(document_id: str) -> dict:
        """Return the edit URL for a Lucidchart document.

        Args:
            document_id: The Lucid document ID.

        Returns:
            Dict with ``document_id`` and ``edit_link``.
        """
        async with LucidClient() as client:
            doc = await client.get_document(document_id)
            return {
                "document_id": document_id,
                "edit_link": doc.get("editUrl", doc.get("editLink", "")),
            }
