"""Async HTTP client for the Figma REST API.

Uses httpx with token authentication via the X-FIGMA-TOKEN header.
Designed to be used as an async context manager so the underlying
connection pool is properly cleaned up.
"""

from __future__ import annotations

import httpx

from config import FIGMA_ACCESS_TOKEN, FIGMA_API_BASE


class FigmaAPIError(Exception):
    """Raised when a Figma API call fails."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Figma API {status_code}: {detail}")


class FigmaClient:
    """Async client for the Figma REST API v1."""

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "FigmaClient":
        self._client = httpx.AsyncClient(
            base_url=FIGMA_API_BASE,
            headers={"X-FIGMA-TOKEN": FIGMA_ACCESS_TOKEN},
            timeout=httpx.Timeout(30.0),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        if self._client:
            await self._client.aclose()
            self._client = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_open(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError(
                "FigmaClient is not open. Use it as an async context manager."
            )
        return self._client

    def _handle_error(self, resp: httpx.Response) -> None:
        """Raise a descriptive error for non-2xx responses."""
        if resp.is_success:
            return

        if resp.status_code == 403:
            raise FigmaAPIError(403, "Authentication failed. Check your FIGMA_ACCESS_TOKEN.")
        if resp.status_code == 404:
            raise FigmaAPIError(404, "File or resource not found. Check the file_key or node_id.")
        if resp.status_code == 429:
            raise FigmaAPIError(429, "Rate limited by Figma API. Wait and retry.")

        # Generic fallback
        try:
            body = resp.json()
            detail = body.get("err", body.get("message", resp.text))
        except Exception:
            detail = resp.text
        raise FigmaAPIError(resp.status_code, str(detail))

    # ------------------------------------------------------------------
    # Public API methods
    # ------------------------------------------------------------------

    async def get_file(self, file_key: str) -> dict:
        """Return file metadata, pages, and component list.

        Fetches the full file tree but requests only structural data
        (geometry=paths is omitted to keep the response lighter).
        """
        client = self._ensure_open()
        resp = await client.get(f"/files/{file_key}")
        self._handle_error(resp)
        return resp.json()

    async def get_file_nodes(self, file_key: str, node_ids: list[str]) -> dict:
        """Return data for specific nodes within a file.

        Parameters
        ----------
        file_key:
            The Figma file key.
        node_ids:
            List of node IDs (e.g. ["1:2", "3:4"]).
        """
        client = self._ensure_open()
        ids_param = ",".join(node_ids)
        resp = await client.get(f"/files/{file_key}/nodes", params={"ids": ids_param})
        self._handle_error(resp)
        return resp.json()

    async def get_comments(self, file_key: str) -> list[dict]:
        """Return all comments on a file.

        Each comment includes author name, content, position, and timestamp.
        """
        client = self._ensure_open()
        resp = await client.get(f"/files/{file_key}/comments")
        self._handle_error(resp)
        data = resp.json()
        return data.get("comments", [])

    async def post_comment(
        self,
        file_key: str,
        message: str,
        position: dict | None = None,
    ) -> dict:
        """Post a comment on a Figma file.

        Parameters
        ----------
        file_key:
            The Figma file key.
        message:
            Comment text.
        position:
            Optional dict with x/y coordinates and optional node_id,
            e.g. {"x": 100, "y": 200, "node_id": "1:2"}.
        """
        client = self._ensure_open()
        body: dict = {"message": message}
        if position:
            # Figma expects client_meta with node_id/node_offset or
            # a Vector2 for absolute positioning.
            body["client_meta"] = position
        resp = await client.post(f"/files/{file_key}/comments", json=body)
        self._handle_error(resp)
        return resp.json()

    async def get_images(
        self,
        file_key: str,
        node_ids: list[str],
        format: str = "png",
        scale: int = 2,
    ) -> dict[str, str | None]:
        """Export nodes as rendered images and return their URLs.

        Parameters
        ----------
        file_key:
            The Figma file key.
        node_ids:
            Node IDs to export.
        format:
            Image format — "png", "jpg", "svg", or "pdf".
        scale:
            Export scale (1-4). Default 2 for retina.

        Returns
        -------
        dict mapping node_id -> image URL (or None on per-node failure).
        """
        client = self._ensure_open()
        ids_param = ",".join(node_ids)
        resp = await client.get(
            f"/images/{file_key}",
            params={"ids": ids_param, "format": format, "scale": scale},
        )
        self._handle_error(resp)
        data = resp.json()
        return data.get("images", {})
