"""Async HTTP client for the Lucid REST API.

Provides a thin wrapper around httpx for creating and managing Lucidchart
documents, pages, and data imports.
"""

from __future__ import annotations

import httpx

from config import LUCID_API_BASE, LUCID_API_TOKEN


class LucidAPIError(Exception):
    """Raised when a Lucid API call fails."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Lucid API error {status_code}: {detail}")


class LucidClient:
    """Async client for the Lucid REST API.

    Usage::

        async with LucidClient() as client:
            doc = await client.create_document("My Flowchart")
    """

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    # -- async context manager --------------------------------------------------

    async def __aenter__(self) -> "LucidClient":
        self._client = httpx.AsyncClient(
            base_url=LUCID_API_BASE,
            headers={
                "Lucid-Api-Token": LUCID_API_TOKEN,
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

    # -- helpers ----------------------------------------------------------------

    def _ensure_client(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError(
                "LucidClient must be used as an async context manager: "
                "'async with LucidClient() as client: ...'"
            )
        return self._client

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict | list | None = None,
        params: dict | None = None,
    ) -> dict:
        client = self._ensure_client()
        response = await client.request(method, path, json=json, params=params)
        if response.status_code >= 400:
            detail = response.text[:500] if response.text else "No response body"
            raise LucidAPIError(response.status_code, detail)
        if response.status_code == 204 or not response.text:
            return {}
        return response.json()

    # -- document operations ----------------------------------------------------

    async def create_document(
        self,
        title: str,
        product: str = "lucidchart",
    ) -> dict:
        """Create a new Lucid document.

        Args:
            title: Document title.
            product: Lucid product — ``"lucidchart"`` (default) or ``"lucidspark"``.

        Returns:
            Dict with ``document_id`` and ``edit_link``.
        """
        data = await self._request(
            "POST",
            "/documents",
            json={"title": title, "product": product},
        )
        return {
            "document_id": data.get("documentId", data.get("id", "")),
            "edit_link": data.get("editUrl", data.get("editLink", "")),
        }

    async def get_document(self, document_id: str) -> dict:
        """Return document metadata.

        Args:
            document_id: The Lucid document ID.

        Returns:
            Full document metadata dict from the API.
        """
        return await self._request("GET", f"/documents/{document_id}")

    async def add_page(self, document_id: str, title: str) -> dict:
        """Add a new page to a document.

        Args:
            document_id: Target document ID.
            title: Page title.

        Returns:
            Dict with ``page_id``.
        """
        data = await self._request(
            "POST",
            f"/documents/{document_id}/pages",
            json={"title": title},
        )
        return {"page_id": data.get("pageId", data.get("id", ""))}

    async def import_data(
        self,
        document_id: str,
        data_format: str,
        data: dict | list,
    ) -> dict:
        """Import structured data into a document for auto-generating diagrams.

        Args:
            document_id: Target document ID.
            data_format: Format descriptor (e.g. ``"csv"``, ``"json"``).
            data: The structured payload to import.

        Returns:
            API response dict.
        """
        return await self._request(
            "POST",
            f"/documents/{document_id}/import",
            json={"format": data_format, "data": data},
        )
