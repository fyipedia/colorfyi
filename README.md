# colorfyi

[![PyPI](https://img.shields.io/pypi/v/colorfyi)](https://pypi.org/project/colorfyi/)
[![Python](https://img.shields.io/pypi/pyversions/colorfyi)](https://pypi.org/project/colorfyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python color engine for developers. Convert between 7 color spaces, check WCAG contrast, generate harmonies and shades, simulate color blindness — all with zero dependencies.

> Try the interactive tools at [colorfyi.com](https://colorfyi.com/)

## Install

```bash
pip install colorfyi
```

## Quick Start

```python
from colorfyi import get_color_info, contrast_ratio, harmonies, generate_shades

# Get comprehensive color info
info = get_color_info("FF6B35")
print(info.rgb)   # RGB(r=255, g=107, b=53)
print(info.hsl)   # HSL(h=16.0, s=100.0, l=60.4)
print(info.cmyk)  # CMYK(c=0.0, m=58.0, y=79.2, k=0.0)

# WCAG contrast check
cr = contrast_ratio("FF6B35", "FFFFFF")
print(cr.ratio)      # 3.38
print(cr.aa_large)   # True

# Color harmonies
h = harmonies("FF6B35")
print(h.complementary)       # ['35C0FF']
print(h.analogous)           # ['FF3535', 'FFA135']

# Tailwind-style shades (50-950)
shades = generate_shades("3498DB")
for shade in shades:
    print(f"{shade.level}: #{shade.hex}")
```

## Advanced Usage

```python
from colorfyi import (
    simulate_color_blindness, compare_colors,
    mix_colors, gradient_steps, text_color_for_bg,
)

# Color blindness simulation (Vienot matrices)
cb = simulate_color_blindness("FF6B35")
print(cb.protanopia)     # How protanopic users see this color
print(cb.deuteranopia)   # How deuteranopic users see this color

# Perceptual color comparison (CIE76 Delta E)
cmp = compare_colors("FF6B35", "3498DB")
print(cmp.delta_e)           # 42.3
print(cmp.delta_e_category)  # "Very Different"

# Mix two colors in Lab space
mixed = mix_colors("FF0000", "0000FF", ratio=0.5)
print(mixed)  # Perceptual midpoint

# Generate smooth gradient
colors = gradient_steps("FF6B35", "3498DB", steps=5)
print(colors)  # ['FF6B35', ..., '3498DB']

# Best text color for a background
print(text_color_for_bg("1A1A2E"))  # "FFFFFF" (white text)
print(text_color_for_bg("F0F0F0"))  # "000000" (black text)
```

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
| `get_color_info(hex) -> ColorInfo` | All color spaces at once |

### WCAG Contrast

| Function | Description |
|----------|-------------|
| `contrast_ratio(hex1, hex2) -> ContrastResult` | WCAG 2.1 contrast ratio + AA/AAA checks |
| `relative_luminance(r, g, b) -> float` | Relative luminance (0-1) |
| `text_color_for_bg(hex) -> str` | Best text color for a background |

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

- **7 color spaces**: RGB, HSL, HSV, CMYK, Lab, OKLCH, Hex
- **WCAG 2.1 contrast**: AA/AAA checks for normal and large text
- **Color harmonies**: complementary, analogous, triadic, split-complementary, tetradic
- **Shade generation**: Tailwind-style 50-950 scale
- **Color blindness simulation**: protanopia, deuteranopia, tritanopia, achromatopsia (Vienot matrices)
- **Perceptual comparison**: CIE76 Delta E, Lab-space gradients and mixing
- **Zero dependencies**: Pure Python, only `math` from stdlib
- **Type-safe**: Full type annotations, `py.typed` marker (PEP 561)

## Related Packages

| Package | Description |
|---------|-------------|
| [emojifyi](https://github.com/fyipedia/emojifyi) | Emoji encoding & metadata for 3,781 emojis |
| [fontfyi](https://github.com/fyipedia/fontfyi) | Google Fonts metadata, CSS helpers, font pairings |
| [symbolfyi](https://github.com/fyipedia/symbolfyi) | Symbol & character encoding (11 formats) |
| [unicodefyi](https://github.com/fyipedia/unicodefyi) | Unicode character toolkit (17 encodings) |

## Links

- [Interactive Color Converter](https://colorfyi.com/) — Convert any color online
- [Contrast Checker](https://colorfyi.com/tools/contrast-checker/) — WCAG accessibility checker
- [API Documentation](https://colorfyi.com/developers/) — REST API with free access
- [Source Code](https://github.com/fyipedia/colorfyi)

## License

MIT
