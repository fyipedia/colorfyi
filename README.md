# colorfyi

[![PyPI](https://img.shields.io/pypi/v/colorfyi)](https://pypi.org/project/colorfyi/)
[![Python](https://img.shields.io/pypi/pyversions/colorfyi)](https://pypi.org/project/colorfyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python color engine for developers. Convert between 7 color spaces (hex, RGB, HSL, HSV, CMYK, CIE Lab, OKLCH), check [WCAG contrast ratios](https://colorfyi.com/tools/contrast-checker/), generate [color harmonies](https://colorfyi.com/tools/palette-generator/) and [Tailwind-style shades](https://colorfyi.com/tools/shade-generator/), simulate [color blindness](https://colorfyi.com/tools/color-blindness-simulator/), and create [smooth gradients](https://colorfyi.com/tools/gradient-generator/) -- all with zero dependencies.

> **Try the interactive tools at [colorfyi.com](https://colorfyi.com/)** -- [color converter](https://colorfyi.com/tools/converter/), [contrast checker](https://colorfyi.com/tools/contrast-checker/), [palette generator](https://colorfyi.com/tools/palette-generator/), [shade generator](https://colorfyi.com/tools/shade-generator/), [color blindness simulator](https://colorfyi.com/tools/color-blindness-simulator/), and [gradient generator](https://colorfyi.com/tools/gradient-generator/).

## Install

```bash
pip install colorfyi                # Core engine (zero deps)
pip install "colorfyi[cli]"         # + Command-line interface
pip install "colorfyi[mcp]"         # + MCP server for AI assistants
pip install "colorfyi[api]"         # + HTTP client for colorfyi.com API
pip install "colorfyi[all]"         # Everything
```

## Quick Start

```python
from colorfyi import get_color_info, contrast_ratio, harmonies, generate_shades

# Convert any hex color to 7 color spaces instantly
info = get_color_info("FF6B35")
print(info.rgb)    # RGB(r=255, g=107, b=53)
print(info.hsl)    # HSL(h=16.0, s=100.0, l=60.4)
print(info.cmyk)   # CMYK(c=0.0, m=58.0, y=79.2, k=0.0)
print(info.oklch)  # OKLCH(l=0.685, c=0.179, h=42.9)

# WCAG 2.1 contrast ratio with AA/AAA compliance checks
cr = contrast_ratio("FF6B35", "FFFFFF")
print(cr.ratio)      # 3.38
print(cr.aa_large)   # True
print(cr.aaa_normal) # False

# Generate all 5 harmony types at once
h = harmonies("FF6B35")
print(h.complementary)       # ['35C0FF']
print(h.analogous)           # ['FF3535', 'FFA135']
print(h.triadic)             # ['6B35FF', '35FF6B']

# Tailwind-style shade palette (50-950)
shades = generate_shades("3498DB")
for shade in shades:
    print(f"{shade.level}: #{shade.hex}")
```

## Color Blindness Simulation

```python
from colorfyi import simulate_color_blindness

# Simulate how 8% of men experience your color choices
cb = simulate_color_blindness("FF6B35")
print(cb.protanopia)     # Red-blind simulation
print(cb.deuteranopia)   # Green-blind simulation
print(cb.tritanopia)     # Blue-blind simulation
print(cb.achromatopsia)  # Total color blindness
```

## Perceptual Color Comparison

```python
from colorfyi import compare_colors, mix_colors, gradient_steps

# CIE76 Delta E perceptual distance
cmp = compare_colors("FF6B35", "3498DB")
print(cmp.delta_e)           # 42.3
print(cmp.delta_e_category)  # "Very Different"

# Mix colors in Lab space (perceptually uniform)
mixed = mix_colors("FF0000", "0000FF", ratio=0.5)

# Smooth gradient with perceptual interpolation
colors = gradient_steps("FF6B35", "3498DB", steps=7)
```

## Command-Line Interface

```bash
pip install "colorfyi[cli]"

colorfyi info FF6B35                    # Full color info table
colorfyi contrast 000000 FFFFFF         # WCAG contrast check
colorfyi harmonies FF6B35               # Color harmonies
colorfyi shades 3B82F6                  # Tailwind shade palette
colorfyi blindness FF5733               # Color blindness simulation
colorfyi mix FF0000 0000FF              # Mix two colors
colorfyi compare FF6B35 3498DB          # Compare two colors
colorfyi gradient FF0000 0000FF         # Smooth gradient
```

## MCP Server (Claude, Cursor, Windsurf)

Add color tools to any AI assistant that supports [Model Context Protocol](https://modelcontextprotocol.io/).

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

**Available tools**: `color_info`, `contrast_check`, `color_harmonies`, `color_shades`, `simulate_color_blindness`, `mix_colors`, `compare_colors`, `gradient`, `text_color_for_background`

## REST API Client

```python
pip install "colorfyi[api]"
```

```python
from colorfyi.api import ColorFYI

with ColorFYI() as api:
    info = api.color("FF6B35")         # GET /api/color/FF6B35/
    cr = api.contrast("000", "FFF")    # GET /api/contrast/?fg=000&bg=FFF
    shades = api.shades("3B82F6")      # GET /api/shades/3B82F6/
    palette = api.palette("FF6B35")    # GET /api/palette/FF6B35/
```

Full [API documentation](https://colorfyi.com/developers/) with OpenAPI spec at [colorfyi.com/api/openapi.json](https://colorfyi.com/api/openapi.json).

## API Reference

### Color Conversion

| Function | Description |
|----------|-------------|
| `hex_to_rgb(hex) -> RGB` | HEX to RGB |
| `rgb_to_hex(r, g, b) -> str` | RGB to HEX |
| `rgb_to_hsl(r, g, b) -> HSL` | RGB to HSL |
| `hsl_to_rgb(h, s, l) -> RGB` | HSL to RGB |
| `rgb_to_hsv(r, g, b) -> HSV` | RGB to HSV |
| `rgb_to_cmyk(r, g, b) -> CMYK` | RGB to CMYK |
| `rgb_to_lab(r, g, b) -> Lab` | RGB to CIE Lab |
| `lab_to_rgb(l, a, b) -> RGB` | CIE Lab to RGB |
| `rgb_to_oklch(r, g, b) -> OKLCH` | RGB to OKLCH |
| `get_color_info(hex) -> ColorInfo` | All 7 color spaces at once |

### WCAG Contrast

| Function | Description |
|----------|-------------|
| `contrast_ratio(hex1, hex2) -> ContrastResult` | WCAG 2.1 contrast ratio + AA/AAA checks |
| `relative_luminance(r, g, b) -> float` | Relative luminance (0-1) |
| `text_color_for_bg(hex) -> str` | Best text color (black or white) for a background |

### Harmonies & Palettes

| Function | Description |
|----------|-------------|
| `harmonies(hex) -> HarmonySet` | All 5 harmony types |
| `complementary(hex) -> list[str]` | Complementary colors |
| `analogous(hex) -> list[str]` | Analogous colors |
| `triadic(hex) -> list[str]` | Triadic colors |
| `split_complementary(hex) -> list[str]` | Split-complementary |
| `tetradic(hex) -> list[str]` | Tetradic (rectangular) |

### Shades & Scales

| Function | Description |
|----------|-------------|
| `generate_shades(hex) -> list[ShadeStep]` | Tailwind-style 50-950 |
| `lightness_scale(hex, steps) -> list[ShadeStep]` | Vary lightness only |
| `saturation_scale(hex, steps) -> list[ShadeStep]` | Vary saturation only |
| `hue_shift_scale(hex, steps) -> list[str]` | Rotate through hue spectrum |
| `monochromatic(hex, count) -> list[str]` | Monochromatic palette |

### Comparison & Mixing

| Function | Description |
|----------|-------------|
| `delta_e(hex1, hex2) -> float` | CIE76 perceptual distance |
| `compare_colors(hex1, hex2) -> CompareResult` | Full comparison report |
| `mix_colors(hex1, hex2, ratio) -> str` | Perceptual mixing in Lab space |
| `gradient_steps(hex1, hex2, steps) -> list[str]` | Smooth gradient |
| `simulate_color_blindness(hex) -> ColorBlindResult` | 4 types of CVD simulation |

## Features

- **7 color spaces**: RGB, HSL, HSV, CMYK, CIE Lab, OKLCH, Hex
- **WCAG 2.1 contrast**: AA/AAA compliance checks for normal and large text
- **Color harmonies**: complementary, analogous, triadic, split-complementary, tetradic
- **Shade generation**: Tailwind-style 50-950 scale
- **Color blindness simulation**: protanopia, deuteranopia, tritanopia, achromatopsia (Vienot matrices)
- **Perceptual comparison**: CIE76 Delta E, Lab-space gradients and mixing
- **CLI**: Rich terminal output with color tables
- **MCP server**: 9 tools for AI assistants (Claude, Cursor, Windsurf)
- **REST API client**: httpx-based client for [colorfyi.com API](https://colorfyi.com/developers/)
- **Zero dependencies**: Core engine uses only `math` from stdlib
- **Type-safe**: Full type annotations, `py.typed` marker (PEP 561)
- **Fast**: All computations under 1ms

## FYIPedia Developer Tools

Part of the [FYIPedia](https://github.com/fyipedia) open-source developer tools ecosystem:

| Package | Description |
|---------|-------------|
| **colorfyi** | [Hex to RGB converter](https://colorfyi.com/tools/converter/), [WCAG contrast checker](https://colorfyi.com/tools/contrast-checker/), [color harmonies](https://colorfyi.com/tools/palette-generator/) |
| [emojifyi](https://emojifyi.com/) | [Emoji encoding](https://emojifyi.com/developers/) & metadata for 3,781 Unicode emojis |
| [symbolfyi](https://symbolfyi.com/) | [Symbol encoder](https://symbolfyi.com/developers/) -- 11 encoding formats for any character |
| [unicodefyi](https://unicodefyi.com/) | [Unicode character lookup](https://unicodefyi.com/developers/) -- 17 encodings + character search |
| [fontfyi](https://fontfyi.com/) | [Google Fonts explorer](https://fontfyi.com/developers/) -- metadata, CSS helpers, font pairings |
| [distancefyi](https://pypi.org/project/distancefyi/) | Haversine distance, bearing, travel times -- [distancefyi.com](https://distancefyi.com/) |
| [timefyi](https://pypi.org/project/timefyi/) | Timezone operations, time differences -- [timefyi.com](https://timefyi.com/) |
| [namefyi](https://pypi.org/project/namefyi/) | Korean romanization, Five Elements -- [namefyi.com](https://namefyi.com/) |
| [unitfyi](https://pypi.org/project/unitfyi/) | Unit conversion, 200 units, 20 categories -- [unitfyi.com](https://unitfyi.com/) |
| [holidayfyi](https://pypi.org/project/holidayfyi/) | Holiday dates, Easter calculation -- [holidayfyi.com](https://holidayfyi.com/) |

## Links

- [Interactive Color Converter](https://colorfyi.com/tools/converter/) -- Convert hex, RGB, HSL, CMYK, OKLCH
- [WCAG Contrast Checker](https://colorfyi.com/tools/contrast-checker/) -- Test color accessibility
- [Palette Generator](https://colorfyi.com/tools/palette-generator/) -- Create color harmonies
- [Shade Generator](https://colorfyi.com/tools/shade-generator/) -- Tailwind-style shade palettes
- [Color Blindness Simulator](https://colorfyi.com/tools/color-blindness-simulator/) -- Test for color vision deficiency
- [Gradient Generator](https://colorfyi.com/tools/gradient-generator/) -- Create smooth CSS gradients
- [REST API Documentation](https://colorfyi.com/developers/) -- Free API with OpenAPI spec
- [Source Code](https://github.com/fyipedia/colorfyi) -- MIT licensed

## License

MIT
