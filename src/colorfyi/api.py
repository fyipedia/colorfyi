"""HTTP API client for colorfyi.com REST endpoints.

Requires the ``api`` extra: ``pip install colorfyi[api]``

Usage::

    from colorfyi.api import ColorFYI

    with ColorFYI() as api:
        items = api.list_brands()
        detail = api.get_brand("example-slug")
        results = api.search("query")
"""

from __future__ import annotations

from typing import Any

import httpx


class ColorFYI:
    """API client for the colorfyi.com REST API.

    Provides typed access to all colorfyi.com endpoints including
    list, detail, and search operations.

    Args:
        base_url: API base URL. Defaults to ``https://colorfyi.com``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://colorfyi.com",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(
            path,
            params={k: v for k, v in params.items() if v is not None},
        )
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -----------------------------------------------------------

    def list_brands(self, **params: Any) -> dict[str, Any]:
        """List all brands."""
        return self._get("/api/v1/brands/", **params)

    def get_brand(self, slug: str) -> dict[str, Any]:
        """Get brand by slug."""
        return self._get(f"/api/v1/brands/" + slug + "/")

    def list_collections(self, **params: Any) -> dict[str, Any]:
        """List all collections."""
        return self._get("/api/v1/collections/", **params)

    def get_collection(self, slug: str) -> dict[str, Any]:
        """Get collection by slug."""
        return self._get(f"/api/v1/collections/" + slug + "/")

    def list_colors(self, **params: Any) -> dict[str, Any]:
        """List all colors."""
        return self._get("/api/v1/colors/", **params)

    def get_color(self, slug: str) -> dict[str, Any]:
        """Get color by slug."""
        return self._get(f"/api/v1/colors/" + slug + "/")

    def list_faqs(self, **params: Any) -> dict[str, Any]:
        """List all faqs."""
        return self._get("/api/v1/faqs/", **params)

    def get_faq(self, slug: str) -> dict[str, Any]:
        """Get faq by slug."""
        return self._get(f"/api/v1/faqs/" + slug + "/")

    def list_glossary(self, **params: Any) -> dict[str, Any]:
        """List all glossary."""
        return self._get("/api/v1/glossary/", **params)

    def get_term(self, slug: str) -> dict[str, Any]:
        """Get term by slug."""
        return self._get(f"/api/v1/glossary/" + slug + "/")

    def list_posts(self, **params: Any) -> dict[str, Any]:
        """List all posts."""
        return self._get("/api/v1/posts/", **params)

    def get_post(self, slug: str) -> dict[str, Any]:
        """Get post by slug."""
        return self._get(f"/api/v1/posts/" + slug + "/")

    def search(self, query: str, **params: Any) -> dict[str, Any]:
        """Search across all content."""
        return self._get(f"/api/v1/search/", q=query, **params)

    # -- Lifecycle -----------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> ColorFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
