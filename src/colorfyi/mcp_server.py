"""MCP server for colorfyi — color tools for AI assistants.

Requires the ``mcp`` extra: ``pip install colorfyi[mcp]``

Run as a standalone server::

    python -m colorfyi.mcp_server

Or configure in ``claude_desktop_config.json``::

    {
        "mcpServers": {
            "colorfyi": {
                "command": "python",
                "args": ["-m", "colorfyi.mcp_server"]
            }
        }
    }
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("colorfyi")


@mcp.tool()
def color_info(hex_code: str) -> str:
    """Get comprehensive information for a hex color.

    Includes RGB, HSL, HSV, CMYK, OKLCH values, plus light/warm properties.

    Args:
        hex_code: Hex color code without # (e.g. "FF6B35").
    """
    from colorfyi import get_color_info

    h = hex_code.lstrip("#").upper()
    ci = get_color_info(h)

    return "\n".join(
        [
            f"## Color #{ci.hex}",
            "",
            "| Property | Value |",
            "|----------|-------|",
            f"| Hex | `#{ci.hex}` |",
            f"| RGB | `rgb({ci.rgb.r}, {ci.rgb.g}, {ci.rgb.b})` |",
            f"| HSL | `hsl({ci.hsl.h:.1f}, {ci.hsl.s:.1f}%, {ci.hsl.l:.1f}%)` |",
            f"| HSV | `hsv({ci.hsv.h:.1f}, {ci.hsv.s:.1f}%, {ci.hsv.v:.1f}%)` |",
            f"| CMYK | `cmyk({ci.cmyk.c:.0f}% {ci.cmyk.m:.0f}%"
            f" {ci.cmyk.y:.0f}% {ci.cmyk.k:.0f}%)` |",
            f"| OKLCH | `oklch({ci.oklch.l:.3f}, {ci.oklch.c:.3f}, {ci.oklch.h:.1f})` |",
            f"| Light | {'Yes' if ci.is_light else 'No'} |",
            f"| Warm | {'Yes' if ci.is_warm else 'No'} |",
        ]
    )


@mcp.tool()
def contrast_check(fg: str, bg: str) -> str:
    """Check WCAG 2.1 contrast ratio between foreground and background colors.

    Returns the contrast ratio and AA/AAA compliance for normal and large text.

    Args:
        fg: Foreground hex color (e.g. "000000").
        bg: Background hex color (e.g. "FFFFFF").
    """
    from colorfyi import contrast_ratio

    cr = contrast_ratio(fg.lstrip("#").upper(), bg.lstrip("#").upper())

    def _pass(v: bool) -> str:
        return "Pass" if v else "Fail"

    return "\n".join(
        [
            f"## Contrast: #{fg.lstrip('#').upper()} on #{bg.lstrip('#').upper()}",
            "",
            f"**Ratio**: {cr.ratio:.2f}:1",
            "",
            "| Level | Result |",
            "|-------|--------|",
            f"| AA Normal | {_pass(cr.aa_normal)} |",
            f"| AA Large | {_pass(cr.aa_large)} |",
            f"| AAA Normal | {_pass(cr.aaa_normal)} |",
            f"| AAA Large | {_pass(cr.aaa_large)} |",
        ]
    )


@mcp.tool()
def color_harmonies(hex_code: str) -> str:
    """Generate color harmonies (complementary, analogous, triadic, split-complementary, tetradic).

    Args:
        hex_code: Hex color code without # (e.g. "3B82F6").
    """
    from colorfyi import harmonies

    h = hex_code.lstrip("#").upper()
    hs = harmonies(h)

    return "\n".join(
        [
            f"## Harmonies for #{h}",
            "",
            "| Type | Colors |",
            "|------|--------|",
            f"| Complementary | {', '.join(f'#{c}' for c in hs.complementary)} |",
            f"| Analogous | {', '.join(f'#{c}' for c in hs.analogous)} |",
            f"| Triadic | {', '.join(f'#{c}' for c in hs.triadic)} |",
            f"| Split Comp. | {', '.join(f'#{c}' for c in hs.split_complementary)} |",
            f"| Tetradic | {', '.join(f'#{c}' for c in hs.tetradic)} |",
        ]
    )


@mcp.tool()
def color_shades(hex_code: str) -> str:
    """Generate Tailwind-style shade palette (50-950) for a color.

    Args:
        hex_code: Hex color code without # (e.g. "3B82F6").
    """
    from colorfyi import generate_shades

    h = hex_code.lstrip("#").upper()
    steps = generate_shades(h)

    lines = [f"## Shades for #{h}", "", "| Level | Hex |", "|-------|-----|"]
    for step in steps:
        lines.append(f"| {step.level} | `#{step.hex}` |")

    return "\n".join(lines)


@mcp.tool()
def simulate_color_blindness(hex_code: str) -> str:
    """Simulate how a color appears under 4 types of color vision deficiency.

    Covers protanopia, deuteranopia, tritanopia, and achromatopsia using Viénot matrices.

    Args:
        hex_code: Hex color code without # (e.g. "FF5733").
    """
    from colorfyi import simulate_color_blindness as _sim

    h = hex_code.lstrip("#").upper()
    cb = _sim(h)

    return "\n".join(
        [
            f"## Color Blindness Simulation for #{h}",
            "",
            "| Type | Simulated |",
            "|------|-----------|",
            f"| Original | `#{cb.original}` |",
            f"| Protanopia | `#{cb.protanopia}` |",
            f"| Deuteranopia | `#{cb.deuteranopia}` |",
            f"| Tritanopia | `#{cb.tritanopia}` |",
            f"| Achromatopsia | `#{cb.achromatopsia}` |",
        ]
    )


@mcp.tool()
def mix_colors(hex1: str, hex2: str, ratio: float = 0.5) -> str:
    """Mix two colors in perceptual Lab space.

    Args:
        hex1: First hex color (e.g. "FF0000").
        hex2: Second hex color (e.g. "0000FF").
        ratio: Mix ratio (0.0 = all hex1, 1.0 = all hex2). Default 0.5.
    """
    from colorfyi import mix_colors as _mix

    h1 = hex1.lstrip("#").upper()
    h2 = hex2.lstrip("#").upper()
    result = _mix(h1, h2, ratio)

    return f"Mix of #{h1} and #{h2} (ratio {ratio}): **#{result}**"


@mcp.tool()
def compare_colors(hex1: str, hex2: str) -> str:
    """Compare two colors — contrast ratio, Delta E perceptual distance, and gradient.

    Args:
        hex1: First hex color (e.g. "FF6B35").
        hex2: Second hex color (e.g. "3498DB").
    """
    from colorfyi import compare_colors as _cmp

    h1 = hex1.lstrip("#").upper()
    h2 = hex2.lstrip("#").upper()
    cmp = _cmp(h1, h2)

    gradient_str = " → ".join(f"#{c}" for c in cmp.gradient)

    return "\n".join(
        [
            f"## Compare #{h1} vs #{h2}",
            "",
            f"- **Contrast ratio**: {cmp.contrast.ratio:.2f}:1",
            f"- **Delta E**: {cmp.delta_e:.1f} ({cmp.delta_e_category})",
            f"- **Mixed**: #{cmp.mixed}",
            f"- **Gradient**: {gradient_str}",
        ]
    )


@mcp.tool()
def gradient(hex1: str, hex2: str, steps: int = 7) -> str:
    """Generate a smooth perceptual gradient between two colors in Lab space.

    Args:
        hex1: Start hex color (e.g. "FF6B35").
        hex2: End hex color (e.g. "3498DB").
        steps: Number of gradient steps (default 7).
    """
    from colorfyi import gradient_steps

    h1 = hex1.lstrip("#").upper()
    h2 = hex2.lstrip("#").upper()
    colors = gradient_steps(h1, h2, steps)

    lines = [f"## Gradient: #{h1} → #{h2}", "", "| Step | Hex |", "|------|-----|"]
    for i, c in enumerate(colors):
        lines.append(f"| {i + 1} | `#{c}` |")

    return "\n".join(lines)


@mcp.tool()
def text_color_for_background(hex_code: str) -> str:
    """Determine the best text color (black or white) for a given background color.

    Uses WCAG relative luminance to decide optimal contrast.

    Args:
        hex_code: Background hex color (e.g. "1A1A2E").
    """
    from colorfyi import text_color_for_bg

    h = hex_code.lstrip("#").upper()
    text = text_color_for_bg(h)

    label = "White" if text == "FFFFFF" else "Black"
    return f"Best text color for #{h} background: **#{text}** ({label})"


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
