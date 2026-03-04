"""colorfyi — Pure Python color engine for developers.

Convert between color spaces (RGB, HSL, HSV, CMYK, Lab, OKLCH),
generate harmonies, Tailwind-style shades, WCAG contrast checks,
color blindness simulation, and perceptual color comparison.

Zero dependencies. <1ms per computation.

Usage::

    from colorfyi import get_color_info, contrast_ratio, harmonies

    info = get_color_info("FF6B35")
    print(info.rgb)  # RGB(r=255, g=107, b=53)
    print(info.hsl)  # HSL(h=16.0, s=100.0, l=60.4)

    cr = contrast_ratio("FF6B35", "FFFFFF")
    print(cr.ratio)      # 3.38
    print(cr.aa_large)   # True

    h = harmonies("FF6B35")
    print(h.complementary)  # ['35C0FF']
"""

from colorfyi.engine import (
    CMYK,
    HSL,
    HSV,
    OKLCH,
    RGB,
    SHADE_LEVELS,
    ColorBlindResult,
    ColorInfo,
    CompareResult,
    ContrastResult,
    HarmonySet,
    Lab,
    ShadeStep,
    analogous,
    color_distance_lab,
    compare_colors,
    complementary,
    contrast_ratio,
    delta_e,
    generate_shades,
    get_color_info,
    gradient_steps,
    harmonies,
    hex_to_rgb,
    hsl_to_rgb,
    hue_shift_scale,
    is_light,
    is_warm,
    lab_to_rgb,
    lightness_scale,
    mix_colors,
    mix_colors_triple,
    monochromatic,
    nearest_named_color,
    relative_luminance,
    rgb_to_cmyk,
    rgb_to_hex,
    rgb_to_hsl,
    rgb_to_hsv,
    rgb_to_lab,
    rgb_to_oklch,
    saturation_scale,
    simulate_color_blindness,
    split_complementary,
    tetradic,
    text_color_for_bg,
    triadic,
)

__version__ = "0.1.0"

__all__ = [
    # Data types
    "RGB",
    "HSL",
    "HSV",
    "CMYK",
    "OKLCH",
    "Lab",
    "ContrastResult",
    "ShadeStep",
    "ColorInfo",
    "HarmonySet",
    "ColorBlindResult",
    "CompareResult",
    # Constants
    "SHADE_LEVELS",
    # Conversions
    "hex_to_rgb",
    "rgb_to_hex",
    "rgb_to_hsl",
    "hsl_to_rgb",
    "rgb_to_hsv",
    "rgb_to_cmyk",
    "rgb_to_lab",
    "lab_to_rgb",
    "rgb_to_oklch",
    # Harmonies
    "complementary",
    "analogous",
    "triadic",
    "split_complementary",
    "tetradic",
    "harmonies",
    # Shades & scales
    "generate_shades",
    "monochromatic",
    "lightness_scale",
    "saturation_scale",
    "hue_shift_scale",
    # WCAG contrast
    "relative_luminance",
    "contrast_ratio",
    "text_color_for_bg",
    # Properties
    "is_light",
    "is_warm",
    # Matching
    "color_distance_lab",
    "nearest_named_color",
    # Comparison & mixing
    "delta_e",
    "gradient_steps",
    "mix_colors",
    "mix_colors_triple",
    "compare_colors",
    # Info
    "get_color_info",
    # Color blindness
    "simulate_color_blindness",
]
