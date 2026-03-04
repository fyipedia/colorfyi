---
name: color-tools
description: Convert colors between 7 color spaces, check WCAG contrast, generate harmonies, Tailwind shades, and simulate color blindness.
---

# Color Tools

Color conversion, accessibility checking, and palette generation powered by [colorfyi](https://colorfyi.com/) -- a pure Python color engine with zero dependencies.

## Setup

Install the MCP server:

```bash
pip install "colorfyi[mcp]"
```

Add to your `claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "colorfyi": {
            "command": "python",
            "args": ["-m", "colorfyi.mcp_server"]
        }
    }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `color_info` | Convert any hex color to RGB, HSL, HSV, CMYK, OKLCH, CIE Lab |
| `contrast_check` | WCAG 2.1 contrast ratio with AA/AAA compliance |
| `color_harmonies` | Complementary, analogous, triadic, split-complementary, tetradic |
| `color_shades` | Tailwind-style shade palette (50-950) |
| `simulate_color_blindness` | Protanopia, deuteranopia, tritanopia, achromatopsia |
| `mix_colors` | Perceptual mixing in CIE Lab space |
| `compare_colors` | Delta E distance, contrast ratio, gradient |
| `gradient` | Smooth perceptual gradient between two colors |
| `text_color_for_background` | Best text color (black/white) for any background |

## When to Use

- Designing UI color schemes or checking accessibility
- Converting between color spaces (hex, RGB, HSL, CMYK, OKLCH)
- Generating Tailwind CSS color palettes
- Testing colors for color vision deficiency
- Creating smooth gradients or mixing colors

## Links

- [Interactive Color Converter](https://colorfyi.com/tools/converter/)
- [WCAG Contrast Checker](https://colorfyi.com/tools/contrast-checker/)
- [Palette Generator](https://colorfyi.com/tools/palette-generator/)
- [API Documentation](https://colorfyi.com/developers/)
- [PyPI Package](https://pypi.org/project/colorfyi/)
