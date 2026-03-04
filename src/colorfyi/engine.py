"""ColorEngine — pure Python color calculations, zero dependencies.

All conversions, harmonies, shade generation, WCAG contrast calculations,
color blindness simulation, and perceptual color comparison.
Designed for <1ms per color computation.
"""

from __future__ import annotations

import math
from typing import NamedTuple


# =============================================================================
# Data types
# =============================================================================
class RGB(NamedTuple):
    r: int
    g: int
    b: int


class HSL(NamedTuple):
    h: float  # 0-360
    s: float  # 0-100
    l: float  # 0-100


class HSV(NamedTuple):
    h: float  # 0-360
    s: float  # 0-100
    v: float  # 0-100


class CMYK(NamedTuple):
    c: float  # 0-100
    m: float  # 0-100
    y: float  # 0-100
    k: float  # 0-100


class OKLCH(NamedTuple):
    l: float  # 0-1 (lightness)
    c: float  # 0-0.4+ (chroma)
    h: float  # 0-360 (hue)


class Lab(NamedTuple):
    l: float  # 0-100
    a: float  # -128 to 127
    b: float  # -128 to 127


class ContrastResult(NamedTuple):
    ratio: float
    aa_normal: bool  # >= 4.5
    aa_large: bool  # >= 3.0
    aaa_normal: bool  # >= 7.0
    aaa_large: bool  # >= 4.5


class ShadeStep(NamedTuple):
    level: int  # 50, 100, 200, ..., 950
    hex: str


class ColorInfo(NamedTuple):
    hex: str
    rgb: RGB
    hsl: HSL
    hsv: HSV
    cmyk: CMYK
    oklch: OKLCH
    is_light: bool
    is_warm: bool


class HarmonySet(NamedTuple):
    complementary: list[str]
    analogous: list[str]
    triadic: list[str]
    split_complementary: list[str]
    tetradic: list[str]


class ColorBlindResult(NamedTuple):
    original: str
    protanopia: str  # No red cones
    deuteranopia: str  # No green cones
    tritanopia: str  # No blue cones
    achromatopsia: str  # Total color blindness


class CompareResult(NamedTuple):
    color1: ColorInfo
    color2: ColorInfo
    contrast: ContrastResult
    delta_e: float  # CIE76 perceptual difference (0=identical, ~100=max)
    delta_e_category: str  # "Identical"/"Similar"/"Noticeable"/"Very Different"
    gradient: list[str]  # 7-step Lab-interpolated gradient (hex values)
    mixed: str  # 50:50 Lab-space mix (hex)


# =============================================================================
# Conversions
# =============================================================================
def hex_to_rgb(hex_value: str) -> RGB:
    """Convert hex string (with or without #) to RGB."""
    h = hex_value.lstrip("#").upper()
    return RGB(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to 6-char uppercase hex string (no #)."""
    return f"{r:02X}{g:02X}{b:02X}"


def rgb_to_hsl(r: int, g: int, b: int) -> HSL:
    """Convert RGB (0-255) to HSL (h: 0-360, s: 0-100, l: 0-100)."""
    r1, g1, b1 = r / 255.0, g / 255.0, b / 255.0
    cmax = max(r1, g1, b1)
    cmin = min(r1, g1, b1)
    delta = cmax - cmin

    ll = (cmax + cmin) / 2.0

    if delta == 0:
        h = 0.0
        s = 0.0
    else:
        s = delta / (1 - abs(2 * ll - 1))
        if cmax == r1:
            h = 60 * (((g1 - b1) / delta) % 6)
        elif cmax == g1:
            h = 60 * (((b1 - r1) / delta) + 2)
        else:
            h = 60 * (((r1 - g1) / delta) + 4)

    if h < 0:
        h += 360

    return HSL(round(h, 1), round(s * 100, 1), round(ll * 100, 1))


def hsl_to_rgb(h: float, s: float, l: float) -> RGB:
    """Convert HSL (h: 0-360, s: 0-100, l: 0-100) to RGB (0-255)."""
    s1 = s / 100.0
    l1 = l / 100.0

    c = (1 - abs(2 * l1 - 1)) * s1
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l1 - c / 2

    if h < 60:
        r1, g1, b1 = c, x, 0.0
    elif h < 120:
        r1, g1, b1 = x, c, 0.0
    elif h < 180:
        r1, g1, b1 = 0.0, c, x
    elif h < 240:
        r1, g1, b1 = 0.0, x, c
    elif h < 300:
        r1, g1, b1 = x, 0.0, c
    else:
        r1, g1, b1 = c, 0.0, x

    return RGB(
        round((r1 + m) * 255),
        round((g1 + m) * 255),
        round((b1 + m) * 255),
    )


def rgb_to_hsv(r: int, g: int, b: int) -> HSV:
    """Convert RGB (0-255) to HSV (h: 0-360, s: 0-100, v: 0-100)."""
    r1, g1, b1 = r / 255.0, g / 255.0, b / 255.0
    cmax = max(r1, g1, b1)
    cmin = min(r1, g1, b1)
    delta = cmax - cmin

    if delta == 0:
        h = 0.0
    elif cmax == r1:
        h = 60 * (((g1 - b1) / delta) % 6)
    elif cmax == g1:
        h = 60 * (((b1 - r1) / delta) + 2)
    else:
        h = 60 * (((r1 - g1) / delta) + 4)

    if h < 0:
        h += 360

    s = 0.0 if cmax == 0 else (delta / cmax)

    return HSV(round(h, 1), round(s * 100, 1), round(cmax * 100, 1))


def rgb_to_cmyk(r: int, g: int, b: int) -> CMYK:
    """Convert RGB (0-255) to CMYK (0-100)."""
    if r == 0 and g == 0 and b == 0:
        return CMYK(0, 0, 0, 100)

    r1, g1, b1 = r / 255.0, g / 255.0, b / 255.0
    k = 1 - max(r1, g1, b1)
    c = (1 - r1 - k) / (1 - k)
    m = (1 - g1 - k) / (1 - k)
    y = (1 - b1 - k) / (1 - k)

    return CMYK(round(c * 100, 1), round(m * 100, 1), round(y * 100, 1), round(k * 100, 1))


def rgb_to_lab(r: int, g: int, b: int) -> Lab:
    """Convert RGB to CIE Lab (via XYZ). Used for perceptual distance."""

    def linearize(v: float) -> float:
        v = v / 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    rl, gl, bl = linearize(r), linearize(g), linearize(b)

    x = rl * 0.4124564 + gl * 0.3575761 + bl * 0.1804375
    y = rl * 0.2126729 + gl * 0.7151522 + bl * 0.0721750
    z = rl * 0.0193339 + gl * 0.1191920 + bl * 0.9503041

    xn, yn, zn = 0.95047, 1.0, 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x / xn), f(y / yn), f(z / zn)

    l_val = 116 * fy - 16
    a_val = 500 * (fx - fy)
    b_val = 200 * (fy - fz)

    return Lab(round(l_val, 2), round(a_val, 2), round(b_val, 2))


def lab_to_rgb(l: float, a: float, b: float) -> RGB:
    """Convert CIE Lab to RGB (via XYZ). Clamps to valid sRGB [0, 255]."""
    xn, yn, zn = 0.95047, 1.0, 1.08883

    fy = (l + 16) / 116
    fx = a / 500 + fy
    fz = fy - b / 200

    def f_inv(t: float) -> float:
        return t**3 if t**3 > 0.008856 else (t - 16 / 116) / 7.787

    x = xn * f_inv(fx)
    y = yn * f_inv(fy)
    z = zn * f_inv(fz)

    rl = x * 3.2404542 + y * -1.5371385 + z * -0.4985314
    gl = x * -0.9692660 + y * 1.8760108 + z * 0.0415560
    bl = x * 0.0556434 + y * -0.2040259 + z * 1.0572252

    def delinearize(v: float) -> int:
        s = 12.92 * v if v <= 0.0031308 else 1.055 * (v ** (1 / 2.4)) - 0.055
        return max(0, min(255, round(s * 255)))

    return RGB(delinearize(rl), delinearize(gl), delinearize(bl))


def rgb_to_oklch(r: int, g: int, b: int) -> OKLCH:
    """Convert RGB to OKLCH (perceptually uniform color space)."""

    def linearize(v: float) -> float:
        v = v / 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    rl, gl, bl = linearize(r), linearize(g), linearize(b)

    ll = 0.4122214708 * rl + 0.5363325363 * gl + 0.0514459929 * bl
    m = 0.2119034982 * rl + 0.6806995451 * gl + 0.1073969566 * bl
    s = 0.0883024619 * rl + 0.2817188376 * gl + 0.6299787005 * bl

    l_ = math.copysign(abs(ll) ** (1 / 3), ll) if ll != 0 else 0
    m_ = math.copysign(abs(m) ** (1 / 3), m) if m != 0 else 0
    s_ = math.copysign(abs(s) ** (1 / 3), s) if s != 0 else 0

    ok_l = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    ok_a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    ok_b = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_

    c = math.sqrt(ok_a**2 + ok_b**2)
    h = math.degrees(math.atan2(ok_b, ok_a)) % 360

    return OKLCH(round(ok_l, 4), round(c, 4), round(h, 1))


# =============================================================================
# Color harmonies (hue rotation on HSL)
# =============================================================================
def _rotate_hue(hex_value: str, degrees: float) -> str:
    """Rotate hue by degrees and return hex."""
    rgb = hex_to_rgb(hex_value)
    hsl = rgb_to_hsl(*rgb)
    new_h = (hsl.h + degrees) % 360
    new_rgb = hsl_to_rgb(new_h, hsl.s, hsl.l)
    return rgb_to_hex(*new_rgb)


def complementary(hex_value: str) -> list[str]:
    """Return complementary color (180 degree rotation)."""
    return [_rotate_hue(hex_value, 180)]


def analogous(hex_value: str) -> list[str]:
    """Return 2 analogous colors (30 degrees each side)."""
    return [_rotate_hue(hex_value, -30), _rotate_hue(hex_value, 30)]


def triadic(hex_value: str) -> list[str]:
    """Return 2 triadic colors (120 degrees apart)."""
    return [_rotate_hue(hex_value, 120), _rotate_hue(hex_value, 240)]


def split_complementary(hex_value: str) -> list[str]:
    """Return 2 split-complementary colors (150 and 210 degrees)."""
    return [_rotate_hue(hex_value, 150), _rotate_hue(hex_value, 210)]


def tetradic(hex_value: str) -> list[str]:
    """Return 3 tetradic colors (90, 180, 270 degrees)."""
    return [
        _rotate_hue(hex_value, 90),
        _rotate_hue(hex_value, 180),
        _rotate_hue(hex_value, 270),
    ]


def harmonies(hex_value: str) -> HarmonySet:
    """Get all harmony types for a color."""
    return HarmonySet(
        complementary=complementary(hex_value),
        analogous=analogous(hex_value),
        triadic=triadic(hex_value),
        split_complementary=split_complementary(hex_value),
        tetradic=tetradic(hex_value),
    )


# =============================================================================
# Tailwind-style shade generation (50-950, 11 steps)
# =============================================================================
SHADE_LEVELS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]


def generate_shades(hex_value: str) -> list[ShadeStep]:
    """Generate Tailwind-style shade scale (50-950) from a base color.

    The base color is placed at 500. Lighter shades increase lightness
    toward white; darker shades decrease toward black.
    """
    rgb = hex_to_rgb(hex_value)
    hsl = rgb_to_hsl(*rgb)
    h, s = hsl.h, hsl.s

    lightness_map: dict[int, float] = {
        50: 97,
        100: 93,
        200: 86,
        300: 76,
        400: 63,
        500: 50,
        600: 40,
        700: 32,
        800: 25,
        900: 19,
        950: 12,
    }

    shades: list[ShadeStep] = []
    for level in SHADE_LEVELS:
        target_l = lightness_map[level]
        sat_factor = 1.0
        if level <= 100:
            sat_factor = 0.85
        elif level >= 900:
            sat_factor = 0.90

        adj_s = min(s * sat_factor, 100)
        new_rgb = hsl_to_rgb(h, adj_s, target_l)
        shades.append(ShadeStep(level=level, hex=rgb_to_hex(*new_rgb)))

    return shades


# =============================================================================
# WCAG contrast
# =============================================================================
def relative_luminance(r: int, g: int, b: int) -> float:
    """Calculate relative luminance per WCAG 2.1."""

    def linearize(v: int) -> float:
        s = v / 255.0
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(hex1: str, hex2: str) -> ContrastResult:
    """Calculate WCAG contrast ratio between two colors."""
    rgb1 = hex_to_rgb(hex1)
    rgb2 = hex_to_rgb(hex2)
    lum1 = relative_luminance(*rgb1)
    lum2 = relative_luminance(*rgb2)

    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    ratio = (lighter + 0.05) / (darker + 0.05)

    return ContrastResult(
        ratio=round(ratio, 2),
        aa_normal=ratio >= 4.5,
        aa_large=ratio >= 3.0,
        aaa_normal=ratio >= 7.0,
        aaa_large=ratio >= 4.5,
    )


def text_color_for_bg(hex_value: str) -> str:
    """Return 'FFFFFF' or '000000' for best text contrast on given background."""
    rgb = hex_to_rgb(hex_value)
    lum = relative_luminance(*rgb)
    return "FFFFFF" if lum < 0.179 else "000000"


# =============================================================================
# Color properties
# =============================================================================
def is_light(hex_value: str) -> bool:
    """Check if a color is perceptually light (luminance > 0.179)."""
    rgb = hex_to_rgb(hex_value)
    return relative_luminance(*rgb) > 0.179


def is_warm(hex_value: str) -> bool:
    """Check if a color is warm (hue in red-yellow range: 0-60 or 300-360)."""
    rgb = hex_to_rgb(hex_value)
    hsl = rgb_to_hsl(*rgb)
    return hsl.h <= 60 or hsl.h >= 300


# =============================================================================
# Nearest named color (CIE Lab Euclidean distance)
# =============================================================================
def color_distance_lab(hex1: str, hex2: str) -> float:
    """Euclidean distance in CIE Lab color space (perceptually uniform)."""
    lab1 = rgb_to_lab(*hex_to_rgb(hex1))
    lab2 = rgb_to_lab(*hex_to_rgb(hex2))
    return math.sqrt((lab1.l - lab2.l) ** 2 + (lab1.a - lab2.a) ** 2 + (lab1.b - lab2.b) ** 2)


def nearest_named_color(hex_value: str, named_colors: dict[str, str]) -> tuple[str, str, float]:
    """Find the nearest named color by Lab distance.

    Args:
        hex_value: Hex color (with or without #).
        named_colors: dict of {name: hex_value} (e.g., {"red": "FF0000"}).

    Returns:
        (name, hex, distance) of the closest match.
    """
    best_name = ""
    best_hex = ""
    best_dist = float("inf")

    for name, nhex in named_colors.items():
        dist = color_distance_lab(hex_value, nhex)
        if dist < best_dist:
            best_dist = dist
            best_name = name
            best_hex = nhex

    return best_name, best_hex, round(best_dist, 2)


# =============================================================================
# Monochromatic palette
# =============================================================================
def monochromatic(hex_value: str, count: int = 5) -> list[str]:
    """Generate monochromatic palette by varying lightness."""
    rgb = hex_to_rgb(hex_value)
    hsl = rgb_to_hsl(*rgb)
    h, s = hsl.h, hsl.s

    step = 80 / (count + 1)
    results: list[str] = []
    for i in range(1, count + 1):
        ll = 10 + step * i
        new_rgb = hsl_to_rgb(h, s, ll)
        results.append(rgb_to_hex(*new_rgb))
    return results


# =============================================================================
# Color scales
# =============================================================================
def lightness_scale(hex_value: str, steps: int = 11) -> list[ShadeStep]:
    """Vary lightness only, keeping hue and saturation constant."""
    rgb = hex_to_rgb(hex_value)
    hsl = rgb_to_hsl(*rgb)
    h, s = hsl.h, hsl.s

    results: list[ShadeStep] = []
    for i, level in enumerate(SHADE_LEVELS[:steps]):
        target_l = 97 - (i * (97 - 5) / (steps - 1)) if steps > 1 else 50
        new_rgb = hsl_to_rgb(h, s, target_l)
        results.append(ShadeStep(level=level, hex=rgb_to_hex(*new_rgb)))
    return results


def saturation_scale(hex_value: str, steps: int = 11) -> list[ShadeStep]:
    """Vary saturation only, keeping hue and lightness constant."""
    rgb = hex_to_rgb(hex_value)
    hsl = rgb_to_hsl(*rgb)
    h, ll = hsl.h, hsl.l

    results: list[ShadeStep] = []
    for i, level in enumerate(SHADE_LEVELS[:steps]):
        target_s = 5 + (i * 95 / (steps - 1)) if steps > 1 else 50
        new_rgb = hsl_to_rgb(h, target_s, ll)
        results.append(ShadeStep(level=level, hex=rgb_to_hex(*new_rgb)))
    return results


def hue_shift_scale(hex_value: str, steps: int = 12) -> list[str]:
    """Rotate hue through the full spectrum, keeping saturation and lightness."""
    results: list[str] = []
    for i in range(steps):
        deg = (360 / steps) * i
        results.append(_rotate_hue(hex_value, deg))
    return results


# =============================================================================
# Color blindness simulation (Viénot matrices)
# =============================================================================
def _apply_matrix(r: int, g: int, b: int, matrix: list[list[float]]) -> RGB:
    """Apply a 3x3 color transformation matrix to RGB values."""
    nr = matrix[0][0] * r + matrix[0][1] * g + matrix[0][2] * b
    ng = matrix[1][0] * r + matrix[1][1] * g + matrix[1][2] * b
    nb = matrix[2][0] * r + matrix[2][1] * g + matrix[2][2] * b
    return RGB(
        max(0, min(255, round(nr))),
        max(0, min(255, round(ng))),
        max(0, min(255, round(nb))),
    )


_PROTANOPIA_MATRIX = [
    [0.56667, 0.43333, 0.0],
    [0.55833, 0.44167, 0.0],
    [0.0, 0.24167, 0.75833],
]
_DEUTERANOPIA_MATRIX = [
    [0.625, 0.375, 0.0],
    [0.70, 0.30, 0.0],
    [0.0, 0.30, 0.70],
]
_TRITANOPIA_MATRIX = [
    [0.95, 0.05, 0.0],
    [0.0, 0.43333, 0.56667],
    [0.0, 0.475, 0.525],
]


def simulate_color_blindness(hex_value: str) -> ColorBlindResult:
    """Simulate how a color appears under different types of color blindness.

    Uses Viénot et al. (1999) simulation matrices.
    """
    rgb = hex_to_rgb(hex_value)
    r, g, b = rgb.r, rgb.g, rgb.b

    proto = _apply_matrix(r, g, b, _PROTANOPIA_MATRIX)
    deuter = _apply_matrix(r, g, b, _DEUTERANOPIA_MATRIX)
    trit = _apply_matrix(r, g, b, _TRITANOPIA_MATRIX)

    gray = round(0.2126 * r + 0.7152 * g + 0.0722 * b)
    achro = RGB(gray, gray, gray)

    return ColorBlindResult(
        original=hex_value,
        protanopia=rgb_to_hex(*proto),
        deuteranopia=rgb_to_hex(*deuter),
        tritanopia=rgb_to_hex(*trit),
        achromatopsia=rgb_to_hex(*achro),
    )


# =============================================================================
# Color comparison & mixing
# =============================================================================
def delta_e(hex1: str, hex2: str) -> float:
    """CIE76 Delta E — perceptual color difference.

    Returns 0.0 for identical colors, typically up to ~100 for maximally different.
    """
    return round(color_distance_lab(hex1, hex2), 2)


def _delta_e_category(de: float) -> str:
    """Categorize Delta E into human-readable description."""
    if de < 1.0:
        return "Identical"
    if de < 5.0:
        return "Similar"
    if de < 25.0:
        return "Noticeable"
    return "Very Different"


def gradient_steps(hex1: str, hex2: str, steps: int = 7) -> list[str]:
    """Generate gradient by interpolating in Lab space.

    Lab interpolation produces perceptually smoother gradients than RGB.
    """
    lab1 = rgb_to_lab(*hex_to_rgb(hex1))
    lab2 = rgb_to_lab(*hex_to_rgb(hex2))

    result: list[str] = []
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0.5
        ll = lab1.l + (lab2.l - lab1.l) * t
        a = lab1.a + (lab2.a - lab1.a) * t
        b = lab1.b + (lab2.b - lab1.b) * t
        rgb = lab_to_rgb(ll, a, b)
        result.append(rgb_to_hex(*rgb))
    return result


def mix_colors(hex1: str, hex2: str, ratio: float = 0.5) -> str:
    """Mix two colors in Lab space.

    ratio=0.0 returns hex1, ratio=1.0 returns hex2, ratio=0.5 is 50:50.
    """
    lab1 = rgb_to_lab(*hex_to_rgb(hex1))
    lab2 = rgb_to_lab(*hex_to_rgb(hex2))
    ll = lab1.l + (lab2.l - lab1.l) * ratio
    a = lab1.a + (lab2.a - lab1.a) * ratio
    b = lab1.b + (lab2.b - lab1.b) * ratio
    rgb = lab_to_rgb(ll, a, b)
    return rgb_to_hex(*rgb)


def mix_colors_triple(hex1: str, hex2: str, hex3: str) -> str:
    """Mix three colors equally in Lab space."""
    lab1 = rgb_to_lab(*hex_to_rgb(hex1))
    lab2 = rgb_to_lab(*hex_to_rgb(hex2))
    lab3 = rgb_to_lab(*hex_to_rgb(hex3))
    ll = (lab1.l + lab2.l + lab3.l) / 3
    a = (lab1.a + lab2.a + lab3.a) / 3
    b = (lab1.b + lab2.b + lab3.b) / 3
    rgb = lab_to_rgb(ll, a, b)
    return rgb_to_hex(*rgb)


def compare_colors(hex1: str, hex2: str) -> CompareResult:
    """Full comparison of two colors."""
    info1 = get_color_info(hex1)
    info2 = get_color_info(hex2)
    cr = contrast_ratio(hex1, hex2)
    de = delta_e(hex1, hex2)
    grad = gradient_steps(hex1, hex2, steps=7)
    mixed = mix_colors(hex1, hex2, 0.5)

    return CompareResult(
        color1=info1,
        color2=info2,
        contrast=cr,
        delta_e=de,
        delta_e_category=_delta_e_category(de),
        gradient=grad,
        mixed=mixed,
    )


# =============================================================================
# Comprehensive color info
# =============================================================================
def get_color_info(hex_value: str) -> ColorInfo:
    """Get comprehensive color information from a hex value."""
    h = hex_value.lstrip("#").upper()
    rgb = hex_to_rgb(h)
    hsl = rgb_to_hsl(*rgb)
    hsv = rgb_to_hsv(*rgb)
    cmyk = rgb_to_cmyk(*rgb)
    oklch = rgb_to_oklch(*rgb)

    return ColorInfo(
        hex=h,
        rgb=rgb,
        hsl=hsl,
        hsv=hsv,
        cmyk=cmyk,
        oklch=oklch,
        is_light=is_light(h),
        is_warm=is_warm(h),
    )
