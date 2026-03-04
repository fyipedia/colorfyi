"""HTTP API client for colorfyi.com REST endpoints.

Requires the ``api`` extra: ``pip install colorfyi[api]``

Usage::

    from colorfyi.api import ColorFYI

    with ColorFYI() as api:
        info = api.color("FF6B35")
        print(info["rgb"])  # {"r": 255, "g": 107, "b": 53}

        cr = api.contrast("000000", "FFFFFF")
        print(cr["ratio"])  # 21.0
"""

from __future__ import annotations

from typing import Any

import httpx


class ColorFYI:
    """API client for the colorfyi.com REST API.

    Args:
        base_url: API base URL. Defaults to ``https://colorfyi.com/api``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://colorfyi.com/api",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    # -- HTTP helpers ----------------------------------------------------------

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(path, params={k: v for k, v in params.items() if v is not None})
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -------------------------------------------------------------

    def color(self, hex_code: str) -> dict[str, Any]:
        """Get comprehensive color information.

        Args:
            hex_code: Hex color code without ``#`` (e.g. ``"FF6B35"``).

        Returns:
            Dict with rgb, hsl, hsv, cmyk, oklch, and more.
        """
        return self._get(f"/color/{hex_code}/")

    def contrast(self, fg: str, bg: str) -> dict[str, Any]:
        """Check WCAG 2.1 contrast ratio between two colors.

        Args:
            fg: Foreground hex color.
            bg: Background hex color.

        Returns:
            Dict with ratio, aa_normal, aa_large, aaa_normal, aaa_large.
        """
        return self._get("/contrast/", fg=fg, bg=bg)

    def search(self, query: str) -> dict[str, Any]:
        """Search named colors by name or hex.

        Args:
            query: Search term (e.g. ``"coral"``, ``"FF"``).
        """
        return self._get("/search/", q=query)

    def harmonies(self, hex_code: str) -> dict[str, Any]:
        """Get color harmonies (complementary, analogous, triadic, etc.).

        Args:
            hex_code: Hex color code without ``#``.
        """
        return self._get(f"/harmonies/{hex_code}/")

    def shades(self, hex_code: str) -> dict[str, Any]:
        """Generate Tailwind-style shade palette (50-950).

        Args:
            hex_code: Hex color code without ``#``.
        """
        return self._get(f"/shades/{hex_code}/")

    def blindness(self, hex_code: str) -> dict[str, Any]:
        """Simulate color blindness (protanopia, deuteranopia, tritanopia).

        Args:
            hex_code: Hex color code without ``#``.
        """
        return self._get(f"/blindness/{hex_code}/")

    def compare(self, hex1: str, hex2: str) -> dict[str, Any]:
        """Compare two colors (contrast, delta E, gradient).

        Args:
            hex1: First hex color.
            hex2: Second hex color.
        """
        return self._get("/compare/", hex1=hex1, hex2=hex2)

    def mix(self, hex1: str, hex2: str, ratio: float = 0.5) -> dict[str, Any]:
        """Mix two colors in perceptual Lab space.

        Args:
            hex1: First hex color.
            hex2: Second hex color.
            ratio: Mix ratio (0.0 = all hex1, 1.0 = all hex2).
        """
        return self._get("/mix/", hex1=hex1, hex2=hex2, ratio=str(ratio))

    def gradient(self, hex1: str, hex2: str, steps: int = 5) -> dict[str, Any]:
        """Generate smooth gradient between two colors.

        Args:
            hex1: Start hex color.
            hex2: End hex color.
            steps: Number of gradient steps.
        """
        return self._get("/gradient/", hex1=hex1, hex2=hex2, steps=str(steps))

    def palette(self, hex_code: str) -> dict[str, Any]:
        """Generate a full palette from a seed color.

        Args:
            hex_code: Hex color code without ``#``.
        """
        return self._get(f"/palette/{hex_code}/")

    def named_colors(self, source: str | None = None) -> dict[str, Any]:
        """Browse named colors (CSS, Tailwind, brand colors).

        Args:
            source: Filter by source (``"css"``, ``"tailwind"``, etc.).
        """
        return self._get("/named-colors/", source=source)

    # -- Context manager -------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP connection."""
        self._client.close()

    def __enter__(self) -> ColorFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
