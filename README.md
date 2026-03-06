# colorfyi

[![PyPI](https://img.shields.io/pypi/v/colorfyi)](https://pypi.org/project/colorfyi/)
[![Python](https://img.shields.io/pypi/pyversions/colorfyi)](https://pypi.org/project/colorfyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)](https://pypi.org/project/colorfyi/)

Pure Python color engine for developers. Convert between 7 color spaces (hex, RGB, HSL, HSV, CMYK, CIE Lab, OKLCH), check [WCAG contrast ratios](https://colorfyi.com/tools/contrast-checker/), generate [color harmonies](https://colorfyi.com/tools/palette-generator/) and [Tailwind-style shades](https://colorfyi.com/tools/shade-generator/), simulate [color blindness](https://colorfyi.com/tools/color-blindness-simulator/), and create [smooth gradients](https://colorfyi.com/tools/gradient-generator/) — all with zero dependencies and sub-millisecond performance.

Extracted from [ColorFYI](https://colorfyi.com/), a color reference platform with 809 named colors across 6 color systems (CSS, X11, Crayola, Pantone, RAL, NCS), 544 brand color palettes, and interactive tools used by developers and designers worldwide.

> **Try the interactive tools at [colorfyi.com](https://colorfyi.com/)** — [color converter](https://colorfyi.com/tools/converter/), [contrast checker](https://colorfyi.com/tools/contrast-checker/), [palette generator](https://colorfyi.com/tools/palette-generator/), [shade generator](https://colorfyi.com/tools/shade-generator/), [color blindness simulator](https://colorfyi.com/tools/color-blindness-simulator/), and [gradient generator](https://colorfyi.com/tools/gradient-generator/).

<p align="center">
  <img src="https://raw.githubusercontent.com/fyipedia/colorfyi/main/demo.gif" alt="colorfyi demo — color conversion, WCAG contrast check, and harmony generation in Python" width="800">
</p>

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [What You Can Do](#what-you-can-do)
  - [Color Space Conversion](#color-space-conversion)
  - [WCAG Contrast Checking](#wcag-contrast-checking)
  - [Color Harmonies](#color-harmonies)
  - [Tailwind-Style Shades](#tailwind-style-shades)
  - [Color Blindness Simulation](#color-blindness-simulation)
  - [Perceptual Color Comparison](#perceptual-color-comparison)
- [Command-Line Interface](#command-line-interface)
- [MCP Server (Claude, Cursor, Windsurf)](#mcp-server-claude-cursor-windsurf)
- [REST API Client](#rest-api-client)
- [API Reference](#api-reference)
- [Learn More About Color](#learn-more-about-color)
- [Also Available](#also-available)
- [Creative FYI Family](#creative-fyi-family)
- [License](#license)

## Install

```bash
pip install colorfyi                # Core engine (zero deps)
pip install "colorfyi[cli]"         # + Command-line interface (typer, rich)
pip install "colorfyi[mcp]"         # + MCP server for AI assistants
pip install "colorfyi[api]"         # + HTTP client for colorfyi.com API
pip install "colorfyi[all]"         # Everything
```

Or run instantly without installing:

```bash
uvx --from colorfyi colorfyi info FF6B35
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
print(h.complementary)  # ['35C0FF']
print(h.analogous)      # ['FF3535', 'FFA135']
print(h.triadic)        # ['6B35FF', '35FF6B']

# Tailwind-style shade palette (50-950)
shades = generate_shades("3498DB")
for shade in shades:
    print(f"{shade.level}: #{shade.hex}")
```

## What You Can Do

### Color Space Conversion

Convert between **7 color spaces** in a single call. Each space has different strengths:

| Color Space | Best For | Example |
|-------------|----------|---------|
| **Hex** | Web/CSS, shorthand notation | `#FF6B35` |
| **RGB** | Screen display, digital design | `rgb(255, 107, 53)` |
| **HSL** | Intuitive hue/saturation/lightness adjustments | `hsl(16°, 100%, 60%)` |
| **HSV** | Color pickers (Photoshop, Figma) | `hsv(16°, 79%, 100%)` |
| **CMYK** | Print design, physical media | `cmyk(0%, 58%, 79%, 0%)` |
| **CIE Lab** | Perceptually uniform comparisons, Delta E | `Lab(65.4, 42.1, 47.8)` |
| **OKLCH** | Modern CSS (`oklch()`), perceptual palettes | `oklch(0.685, 0.179, 42.9)` |

```python
from colorfyi import get_color_info

info = get_color_info("3B82F6")  # Tailwind Blue 500
print(info.rgb)    # RGB(r=59, g=130, b=246)
print(info.hsl)    # HSL(h=217.2, s=91.2, l=59.8)
print(info.oklch)  # OKLCH(l=0.623, c=0.184, h=259.1)
```

Learn more: [Color Converter Tool](https://colorfyi.com/tools/converter/) · [What is OKLCH?](https://colorfyi.com/blog/oklch-color-space/) · [Color Space Guide](https://colorfyi.com/glossary/terms/color-space/)

### WCAG Contrast Checking

Test color pairs against [WCAG 2.1 accessibility guidelines](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html). The Web Content Accessibility Guidelines require a minimum contrast ratio of **4.5:1** for normal text (AA) and **7:1** for enhanced contrast (AAA).

```python
from colorfyi import contrast_ratio, text_color_for_bg

# Check if your color combination is accessible
cr = contrast_ratio("1E40AF", "FFFFFF")  # Dark blue on white
print(cr.ratio)       # 8.55
print(cr.aa_normal)   # True  (≥ 4.5:1)
print(cr.aa_large)    # True  (≥ 3:1)
print(cr.aaa_normal)  # True  (≥ 7:1)
print(cr.aaa_large)   # True  (≥ 4.5:1)

# Automatically pick black or white text for any background
text = text_color_for_bg("FF6B35")  # → "000000" (black text)
text = text_color_for_bg("1E3A5F")  # → "FFFFFF" (white text)
```

Learn more: [WCAG Contrast Checker](https://colorfyi.com/tools/contrast-checker/) · [Contrast Ratio Guide](https://colorfyi.com/glossary/terms/contrast-ratio/)

### Color Harmonies

Generate aesthetically pleasing color combinations based on **color wheel theory**. Five harmony types cover different design needs:

| Harmony | Description | Use Case |
|---------|-------------|----------|
| **Complementary** | Opposite on the color wheel | High contrast, bold designs |
| **Analogous** | Adjacent colors (±30°) | Cohesive, harmonious palettes |
| **Triadic** | Three evenly spaced (120°) | Vibrant, balanced layouts |
| **Split-complementary** | Complement + neighbors | Softer contrast than complementary |
| **Tetradic** | Four colors (rectangle) | Rich, complex color schemes |

```python
from colorfyi import harmonies

h = harmonies("FF6B35")
print(h.complementary)        # ['35C0FF']
print(h.analogous)            # ['FF3535', 'FFA135']
print(h.triadic)              # ['6B35FF', '35FF6B']
print(h.split_complementary)  # ['3565FF', '35FFA1']
print(h.tetradic)             # ['C035FF', '35FF6B', '35C0FF']
```

Learn more: [Palette Generator](https://colorfyi.com/tools/palette-generator/) · [Color Harmony Guide](https://colorfyi.com/glossary/terms/color-harmony/)

### Tailwind-Style Shades

Generate a full 50–950 shade scale from any base color, matching Tailwind CSS conventions. Essential for building design systems and consistent UI themes.

```python
from colorfyi import generate_shades

shades = generate_shades("3B82F6")  # Generate shades from Tailwind Blue 500
# shade.level: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950
for shade in shades:
    print(f"{shade.level}: #{shade.hex}")
```

Learn more: [Shade Generator](https://colorfyi.com/tools/shade-generator/) · [Tailwind CSS Colors](https://colorfyi.com/collections/tailwind-css/)

### Color Blindness Simulation

Approximately **8% of men and 0.5% of women** have some form of color vision deficiency (CVD). Simulate how your colors appear to users with different types of color blindness using Viénot transformation matrices.

```python
from colorfyi import simulate_color_blindness

cb = simulate_color_blindness("FF6B35")
print(cb.protanopia)     # Red-blind (~1% of men)
print(cb.deuteranopia)   # Green-blind (~6% of men, most common)
print(cb.tritanopia)     # Blue-blind (rare, ~0.01%)
print(cb.achromatopsia)  # Total color blindness (monochromacy)
```

Learn more: [Color Blindness Simulator](https://colorfyi.com/tools/color-blindness-simulator/) · [Color Vision Deficiency Guide](https://colorfyi.com/glossary/terms/color-blindness/)

### Perceptual Color Comparison

Compare colors using **CIE76 Delta E** — a metric designed to match human perception. Unlike simple RGB distance, Delta E accounts for how our eyes actually perceive color differences.

| Delta E | Perception |
|---------|-----------|
| 0–1 | Not perceptible |
| 1–2 | Barely perceptible |
| 2–10 | Perceptible at close look |
| 10–50 | Clearly different |
| 50+ | Very different |

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

Learn more: [Gradient Generator](https://colorfyi.com/tools/gradient-generator/) · [Delta E Explained](https://colorfyi.com/glossary/terms/delta-e/)

## Command-Line Interface

```bash
pip install "colorfyi[cli]"

colorfyi info FF6B35                    # Full color info (7 spaces)
colorfyi contrast 000000 FFFFFF         # WCAG contrast check
colorfyi harmonies FF6B35               # Color harmonies
colorfyi shades 3B82F6                  # Tailwind shade palette
colorfyi blindness FF5733               # Color blindness simulation
colorfyi mix FF0000 0000FF              # Mix two colors
colorfyi compare FF6B35 3498DB          # Compare (Delta E)
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
            "command": "uvx",
            "args": ["--from", "colorfyi[mcp]", "python", "-m", "colorfyi.mcp_server"]
        }
    }
}
```

**9 tools available**: `color_info`, `contrast_check`, `color_harmonies`, `color_shades`, `simulate_color_blindness`, `mix_colors`, `compare_colors`, `gradient`, `text_color_for_background`

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
| `relative_luminance(r, g, b) -> float` | Relative luminance (0–1) |
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
| `generate_shades(hex) -> list[ShadeStep]` | Tailwind-style 50–950 |
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

## Learn More About Color

- **Tools**: [Color Converter](https://colorfyi.com/tools/converter/) · [Contrast Checker](https://colorfyi.com/tools/contrast-checker/) · [Palette Generator](https://colorfyi.com/tools/palette-generator/) · [Shade Generator](https://colorfyi.com/tools/shade-generator/) · [Blindness Simulator](https://colorfyi.com/tools/color-blindness-simulator/) · [Gradient Generator](https://colorfyi.com/tools/gradient-generator/)
- **Color Systems**: [CSS Named Colors](https://colorfyi.com/color/named/?source=css) · [Pantone Colors](https://colorfyi.com/collections/pantone/) · [Tailwind Colors](https://colorfyi.com/collections/tailwind-css/) · [RAL Colors](https://colorfyi.com/collections/ral-classic/)
- **Brand Colors**: [544 Brand Palettes](https://colorfyi.com/brands/) · [Google](https://colorfyi.com/brands/google/) · [Apple](https://colorfyi.com/brands/apple/) · [Meta](https://colorfyi.com/brands/meta/)
- **Guides**: [Color Theory Glossary](https://colorfyi.com/glossary/) · [Blog](https://colorfyi.com/blog/)
- **API**: [REST API Docs](https://colorfyi.com/developers/) · [OpenAPI Spec](https://colorfyi.com/api/openapi.json)

## Also Available

| Platform | Install | Link |
|----------|---------|------|
| **npm** | `npm install @fyipedia/colorfyi` | [npm](https://www.npmjs.com/package/@fyipedia/colorfyi) |
| **Homebrew** | `brew tap fyipedia/tap && brew install fyipedia` | [Tap](https://github.com/fyipedia/homebrew-tap) |
| **MCP** | `uvx --from "colorfyi[mcp]" python -m colorfyi.mcp_server` | [Config](#mcp-server-claude-cursor-windsurf) |
| **VSCode** | `ext install fyipedia.colorfyi-vscode` | [Marketplace](https://marketplace.visualstudio.com/items?itemName=fyipedia.colorfyi-vscode) |

## Creative FYI Family

Part of the [FYIPedia](https://fyipedia.com) open-source developer tools ecosystem — design, typography, and character encoding.

| Package | PyPI | npm | Description |
|---------|------|-----|-------------|
| **colorfyi** | [PyPI](https://pypi.org/project/colorfyi/) | [npm](https://www.npmjs.com/package/@fyipedia/colorfyi) | **Color conversion, WCAG contrast, harmonies -- [colorfyi.com](https://colorfyi.com/)** |
| emojifyi | [PyPI](https://pypi.org/project/emojifyi/) | [npm](https://www.npmjs.com/package/emojifyi) | Emoji encoding & metadata for 3,953 emojis -- [emojifyi.com](https://emojifyi.com/) |
| symbolfyi | [PyPI](https://pypi.org/project/symbolfyi/) | [npm](https://www.npmjs.com/package/symbolfyi) | Symbol encoding in 11 formats -- [symbolfyi.com](https://symbolfyi.com/) |
| unicodefyi | [PyPI](https://pypi.org/project/unicodefyi/) | [npm](https://www.npmjs.com/package/unicodefyi) | Unicode lookup with 17 encodings -- [unicodefyi.com](https://unicodefyi.com/) |
| fontfyi | [PyPI](https://pypi.org/project/fontfyi/) | [npm](https://www.npmjs.com/package/fontfyi) | Google Fonts metadata & CSS -- [fontfyi.com](https://fontfyi.com/) |

## License

MIT
