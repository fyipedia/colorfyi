"""Tests for colorfyi.cli — command-line interface."""

from __future__ import annotations

from typer.testing import CliRunner

from colorfyi.cli import app

runner = CliRunner()


class TestCLIInfo:
    def test_info_basic(self) -> None:
        result = runner.invoke(app, ["info", "FF6B35"])
        assert result.exit_code == 0
        assert "FF6B35" in result.output

    def test_info_with_hash(self) -> None:
        result = runner.invoke(app, ["info", "#3B82F6"])
        assert result.exit_code == 0
        assert "3B82F6" in result.output


class TestCLIContrast:
    def test_contrast(self) -> None:
        result = runner.invoke(app, ["contrast", "000000", "FFFFFF"])
        assert result.exit_code == 0
        assert "21" in result.output  # ratio ~21:1

    def test_contrast_fail(self) -> None:
        result = runner.invoke(app, ["contrast", "CCCCCC", "FFFFFF"])
        assert result.exit_code == 0
        assert "Fail" in result.output


class TestCLIHarmonies:
    def test_harmonies(self) -> None:
        result = runner.invoke(app, ["harmonies", "FF6B35"])
        assert result.exit_code == 0
        assert "Complementary" in result.output
        assert "Analogous" in result.output


class TestCLIShades:
    def test_shades(self) -> None:
        result = runner.invoke(app, ["shades", "3B82F6"])
        assert result.exit_code == 0
        assert "50" in result.output
        assert "950" in result.output


class TestCLIBlindness:
    def test_blindness(self) -> None:
        result = runner.invoke(app, ["blindness", "FF5733"])
        assert result.exit_code == 0
        assert "Protanopia" in result.output
        assert "Deuteranopia" in result.output


class TestCLIMix:
    def test_mix(self) -> None:
        result = runner.invoke(app, ["mix", "FF0000", "0000FF"])
        assert result.exit_code == 0
        assert "#" in result.output


class TestCLICompare:
    def test_compare(self) -> None:
        result = runner.invoke(app, ["compare", "FF6B35", "3498DB"])
        assert result.exit_code == 0
        assert "Delta E" in result.output


class TestCLIGradient:
    def test_gradient(self) -> None:
        result = runner.invoke(app, ["gradient", "FF0000", "0000FF"])
        assert result.exit_code == 0
        assert "Step" in result.output


class TestCLINoArgs:
    def test_no_args_shows_help(self) -> None:
        result = runner.invoke(app, [])
        # Typer no_args_is_help=True returns exit code 0 or 2 depending on version
        assert result.exit_code in (0, 2)
        assert "Usage" in result.output or "colorfyi" in result.output.lower()
