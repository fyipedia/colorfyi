"""Tests for colorfyi.api — HTTP client for colorfyi.com."""

from __future__ import annotations

from colorfyi.api import ColorFYI


class TestColorFYIClient:
    """Verify the client initializes and has all expected methods."""

    def test_init_default(self) -> None:
        client = ColorFYI()
        assert str(client._client.base_url) == "https://colorfyi.com/api/"
        client.close()

    def test_init_custom_url(self) -> None:
        client = ColorFYI(base_url="http://localhost:8000/api", timeout=5.0)
        assert "localhost" in str(client._client.base_url)
        client.close()

    def test_context_manager(self) -> None:
        with ColorFYI() as client:
            assert client is not None

    def test_has_all_methods(self) -> None:
        client = ColorFYI()
        methods = [
            "color",
            "contrast",
            "search",
            "harmonies",
            "shades",
            "blindness",
            "compare",
            "mix",
            "gradient",
            "palette",
            "named_colors",
        ]
        for method in methods:
            assert hasattr(client, method), f"Missing method: {method}"
            assert callable(getattr(client, method))
        client.close()
