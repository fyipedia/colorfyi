"""Tests for colorfyi.mcp_server — MCP tools."""

from __future__ import annotations

from colorfyi.mcp_server import (
    color_harmonies,
    color_info,
    color_shades,
    compare_colors,
    contrast_check,
    gradient,
    mix_colors,
    simulate_color_blindness,
    text_color_for_background,
)


class TestMCPColorInfo:
    def test_returns_markdown_table(self) -> None:
        result = color_info("FF6B35")
        assert "## Color #FF6B35" in result
        assert "RGB" in result
        assert "HSL" in result
        assert "CMYK" in result

    def test_strips_hash(self) -> None:
        result = color_info("#3B82F6")
        assert "## Color #3B82F6" in result


class TestMCPContrastCheck:
    def test_high_contrast(self) -> None:
        result = contrast_check("000000", "FFFFFF")
        assert "21.00:1" in result
        assert "Pass" in result

    def test_low_contrast(self) -> None:
        result = contrast_check("CCCCCC", "FFFFFF")
        assert "Fail" in result


class TestMCPHarmonies:
    def test_returns_all_types(self) -> None:
        result = color_harmonies("FF6B35")
        assert "Complementary" in result
        assert "Analogous" in result
        assert "Triadic" in result
        assert "Split Comp." in result
        assert "Tetradic" in result


class TestMCPShades:
    def test_returns_shade_table(self) -> None:
        result = color_shades("3B82F6")
        assert "50" in result
        assert "950" in result


class TestMCPBlindness:
    def test_returns_all_types(self) -> None:
        result = simulate_color_blindness("FF5733")
        assert "Protanopia" in result
        assert "Deuteranopia" in result
        assert "Tritanopia" in result
        assert "Achromatopsia" in result


class TestMCPMix:
    def test_mix(self) -> None:
        result = mix_colors("FF0000", "0000FF")
        assert "Mix of" in result
        assert "#" in result


class TestMCPCompare:
    def test_compare(self) -> None:
        result = compare_colors("FF6B35", "3498DB")
        assert "Contrast ratio" in result
        assert "Delta E" in result
        assert "Gradient" in result


class TestMCPGradient:
    def test_gradient(self) -> None:
        result = gradient("FF0000", "0000FF", steps=5)
        assert "Gradient" in result
        assert "Step" in result


class TestMCPTextColor:
    def test_dark_background(self) -> None:
        result = text_color_for_background("1A1A2E")
        assert "FFFFFF" in result
        assert "White" in result

    def test_light_background(self) -> None:
        result = text_color_for_background("F0F0F0")
        assert "000000" in result
        assert "Black" in result
