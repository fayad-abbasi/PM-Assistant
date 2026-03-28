"""Async HTTP client for the Miro REST API v2."""

from __future__ import annotations

from typing import Any

import httpx

from config import MIRO_ACCESS_TOKEN, MIRO_API_BASE


class MiroClient:
    """Thin async wrapper around the Miro REST API v2.

    Usage::

        async with MiroClient() as miro:
            board = await miro.create_board("My Board")
    """

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    # -- async context manager ------------------------------------------------

    async def __aenter__(self) -> "MiroClient":
        self._client = httpx.AsyncClient(
            base_url=MIRO_API_BASE,
            headers={
                "Authorization": f"Bearer {MIRO_ACCESS_TOKEN}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=30.0,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        if self._client:
            await self._client.aclose()
            self._client = None

    # -- helpers --------------------------------------------------------------

    def _ensure_client(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError("MiroClient must be used as an async context manager.")
        return self._client

    @staticmethod
    def _raise_for_status(response: httpx.Response) -> None:
        """Raise informative errors for common failure modes."""
        if response.status_code == 401:
            raise PermissionError(
                "Miro API returned 401 Unauthorized. Check your MIRO_ACCESS_TOKEN."
            )
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After", "unknown")
            raise RuntimeError(
                f"Miro API rate limit exceeded. Retry after {retry_after}s."
            )
        response.raise_for_status()

    # -- board operations -----------------------------------------------------

    async def create_board(
        self, name: str, description: str | None = None
    ) -> dict[str, Any]:
        """Create a new Miro board.

        Returns a dict with ``board_id`` and ``view_link``.
        """
        client = self._ensure_client()
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description

        resp = await client.post("/boards", json=payload)
        self._raise_for_status(resp)
        data = resp.json()
        return {
            "board_id": data["id"],
            "view_link": data.get("viewLink", ""),
        }

    async def get_board(self, board_id: str) -> dict[str, Any]:
        """Return full board metadata."""
        client = self._ensure_client()
        resp = await client.get(f"/boards/{board_id}")
        self._raise_for_status(resp)
        return resp.json()

    async def get_board_items(self, board_id: str) -> list[dict[str, Any]]:
        """Return all items on a board."""
        client = self._ensure_client()
        resp = await client.get(f"/boards/{board_id}/items")
        self._raise_for_status(resp)
        return resp.json().get("data", [])

    # -- item operations ------------------------------------------------------

    async def create_sticky_note(
        self,
        board_id: str,
        content: str,
        color: str = "yellow",
        x: float = 0,
        y: float = 0,
    ) -> dict[str, Any]:
        """Create a sticky note on *board_id*.

        Returns a dict with ``item_id``.
        """
        client = self._ensure_client()
        payload = {
            "data": {"content": content, "shape": "square"},
            "style": {"fillColor": color},
            "position": {"x": x, "y": y},
        }
        resp = await client.post(
            f"/boards/{board_id}/sticky_notes", json=payload
        )
        self._raise_for_status(resp)
        return {"item_id": resp.json()["id"]}

    async def create_shape(
        self,
        board_id: str,
        content: str,
        shape: str = "rectangle",
        x: float = 0,
        y: float = 0,
        width: float = 200,
        height: float = 100,
    ) -> dict[str, Any]:
        """Create a shape on *board_id*.

        Returns a dict with ``item_id``.
        """
        client = self._ensure_client()
        payload = {
            "data": {"content": content, "shape": shape},
            "position": {"x": x, "y": y},
            "geometry": {"width": width, "height": height},
        }
        resp = await client.post(f"/boards/{board_id}/shapes", json=payload)
        self._raise_for_status(resp)
        return {"item_id": resp.json()["id"]}

    async def create_connector(
        self,
        board_id: str,
        start_item_id: str,
        end_item_id: str,
    ) -> dict[str, Any]:
        """Draw a connector between two items.

        Returns a dict with ``connector_id``.
        """
        client = self._ensure_client()
        payload = {
            "startItem": {"id": start_item_id},
            "endItem": {"id": end_item_id},
        }
        resp = await client.post(
            f"/boards/{board_id}/connectors", json=payload
        )
        self._raise_for_status(resp)
        return {"connector_id": resp.json()["id"]}
