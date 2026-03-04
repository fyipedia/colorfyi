"""Tests for colorfyi engine."""

from __future__ import annotations

from colorfyi import (
    CMYK,
    HSL,
    HSV,
    OKLCH,
    RGB,
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


# =============================================================================
# Conversions
# =============================================================================
class TestHexRGB:
    def test_hex_to_rgb(self) -> None:
        assert hex_to_rgb("FF0000") == RGB(255, 0, 0)
        assert hex_to_rgb("#00ff00") == RGB(0, 255, 0)
        assert hex_to_rgb("0000FF") == RGB(0, 0, 255)

    def test_rgb_to_hex(self) -> None:
        assert rgb_to_hex(255, 0, 0) == "FF0000"
        assert rgb_to_hex(0, 255, 0) == "00FF00"
        assert rgb_to_hex(0, 0, 0) == "000000"
        assert rgb_to_hex(255, 255, 255) == "FFFFFF"

    def test_roundtrip(self) -> None:
        for hex_val in ["FF6B35", "3498DB", "2ECC71", "000000", "FFFFFF"]:
            rgb = hex_to_rgb(hex_val)
            assert rgb_to_hex(*rgb) == hex_val


class TestHSL:
    def test_rgb_to_hsl_red(self) -> None:
        hsl = rgb_to_hsl(255, 0, 0)
        assert hsl.h == 0.0
        assert hsl.s == 100.0
        assert hsl.l == 50.0

    def test_rgb_to_hsl_white(self) -> None:
        hsl = rgb_to_hsl(255, 255, 255)
        assert hsl.l == 100.0
        assert hsl.s == 0.0

    def test_roundtrip(self) -> None:
        original = RGB(100, 150, 200)
        hsl = rgb_to_hsl(*original)
        result = hsl_to_rgb(hsl.h, hsl.s, hsl.l)
        assert abs(result.r - original.r) <= 1
        assert abs(result.g - original.g) <= 1
        assert abs(result.b - original.b) <= 1


class TestHSV:
    def test_pure_red(self) -> None:
        hsv = rgb_to_hsv(255, 0, 0)
        assert hsv.h == 0.0
        assert hsv.s == 100.0
        assert hsv.v == 100.0

    def test_black(self) -> None:
        hsv = rgb_to_hsv(0, 0, 0)
        assert hsv.v == 0.0


class TestCMYK:
    def test_red(self) -> None:
        cmyk = rgb_to_cmyk(255, 0, 0)
        assert cmyk.c == 0
        assert cmyk.m == 100
        assert cmyk.y == 100
        assert cmyk.k == 0

    def test_black(self) -> None:
        cmyk = rgb_to_cmyk(0, 0, 0)
        assert cmyk == CMYK(0, 0, 0, 100)


class TestLab:
    def test_white(self) -> None:
        lab = rgb_to_lab(255, 255, 255)
        assert abs(lab.l - 100) < 1

    def test_black(self) -> None:
        lab = rgb_to_lab(0, 0, 0)
        assert abs(lab.l) < 1

    def test_roundtrip(self) -> None:
        original = RGB(100, 150, 200)
        lab = rgb_to_lab(*original)
        result = lab_to_rgb(lab.l, lab.a, lab.b)
        assert abs(result.r - original.r) <= 1
        assert abs(result.g - original.g) <= 1
        assert abs(result.b - original.b) <= 1


class TestOKLCH:
    def test_white(self) -> None:
        oklch = rgb_to_oklch(255, 255, 255)
        assert oklch.l > 0.99

    def test_black(self) -> None:
        oklch = rgb_to_oklch(0, 0, 0)
        assert oklch.l == 0.0


# =============================================================================
# Harmonies
# =============================================================================
class TestHarmonies:
    def test_complementary(self) -> None:
        result = complementary("FF0000")
        assert len(result) == 1

    def test_analogous(self) -> None:
        assert len(analogous("FF0000")) == 2

    def test_triadic(self) -> None:
        assert len(triadic("FF0000")) == 2

    def test_split_complementary(self) -> None:
        assert len(split_complementary("FF0000")) == 2

    def test_tetradic(self) -> None:
        assert len(tetradic("FF0000")) == 3

    def test_harmony_set(self) -> None:
        h = harmonies("3498DB")
        assert isinstance(h, HarmonySet)
        assert len(h.complementary) == 1
        assert len(h.analogous) == 2
        assert len(h.triadic) == 2
        assert len(h.tetradic) == 3


# =============================================================================
# Shades & Scales
# =============================================================================
class TestShades:
    def test_generate_shades(self) -> None:
        shades = generate_shades("3498DB")
        assert len(shades) == 11
        assert shades[0].level == 50
        assert shades[-1].level == 950
        assert all(isinstance(s, ShadeStep) for s in shades)

    def test_monochromatic(self) -> None:
        palette = monochromatic("FF0000", count=5)
        assert len(palette) == 5

    def test_lightness_scale(self) -> None:
        scale = lightness_scale("3498DB")
        assert len(scale) == 11

    def test_saturation_scale(self) -> None:
        scale = saturation_scale("3498DB")
        assert len(scale) == 11

    def test_hue_shift_scale(self) -> None:
        scale = hue_shift_scale("FF0000", steps=12)
        assert len(scale) == 12
        # First color should be the original
        assert scale[0] == "FF0000"


# =============================================================================
# WCAG Contrast
# =============================================================================
class TestContrast:
    def test_black_white(self) -> None:
        cr = contrast_ratio("000000", "FFFFFF")
        assert cr.ratio == 21.0
        assert cr.aa_normal is True
        assert cr.aaa_normal is True

    def test_same_color(self) -> None:
        cr = contrast_ratio("FF0000", "FF0000")
        assert cr.ratio == 1.0
        assert cr.aa_normal is False

    def test_text_color_for_bg(self) -> None:
        assert text_color_for_bg("000000") == "FFFFFF"
        assert text_color_for_bg("FFFFFF") == "000000"

    def test_relative_luminance_white(self) -> None:
        assert abs(relative_luminance(255, 255, 255) - 1.0) < 0.01

    def test_relative_luminance_black(self) -> None:
        assert relative_luminance(0, 0, 0) == 0.0


# =============================================================================
# Properties
# =============================================================================
class TestProperties:
    def test_is_light(self) -> None:
        assert is_light("FFFFFF") is True
        assert is_light("000000") is False

    def test_is_warm(self) -> None:
        assert is_warm("FF0000") is True
        assert is_warm("0000FF") is False


# =============================================================================
# Matching
# =============================================================================
class TestMatching:
    def test_color_distance_same(self) -> None:
        assert color_distance_lab("FF0000", "FF0000") == 0.0

    def test_nearest_named(self) -> None:
        colors = {"red": "FF0000", "green": "00FF00", "blue": "0000FF"}
        name, _hex_val, dist = nearest_named_color("FE0000", colors)
        assert name == "red"
        assert dist < 2.0


# =============================================================================
# Comparison & Mixing
# =============================================================================
class TestComparison:
    def test_delta_e_identical(self) -> None:
        assert delta_e("FF0000", "FF0000") == 0.0

    def test_delta_e_different(self) -> None:
        de = delta_e("FF0000", "0000FF")
        assert de > 50

    def test_gradient_steps(self) -> None:
        grad = gradient_steps("000000", "FFFFFF", steps=5)
        assert len(grad) == 5
        assert grad[0] == "000000"
        assert grad[-1] == "FFFFFF"

    def test_mix_colors(self) -> None:
        mixed = mix_colors("000000", "FFFFFF", 0.5)
        # Should be a gray
        rgb = hex_to_rgb(mixed)
        assert abs(rgb.r - rgb.g) <= 1
        assert abs(rgb.g - rgb.b) <= 1

    def test_mix_colors_triple(self) -> None:
        mixed = mix_colors_triple("FF0000", "00FF00", "0000FF")
        assert len(mixed) == 6

    def test_compare_colors(self) -> None:
        result = compare_colors("FF0000", "0000FF")
        assert isinstance(result, CompareResult)
        assert isinstance(result.color1, ColorInfo)
        assert isinstance(result.contrast, ContrastResult)
        assert result.delta_e > 0
        assert len(result.gradient) == 7
        assert len(result.mixed) == 6


# =============================================================================
# Color blindness
# =============================================================================
class TestColorBlindness:
    def test_simulate(self) -> None:
        result = simulate_color_blindness("FF0000")
        assert isinstance(result, ColorBlindResult)
        assert result.original == "FF0000"
        # Gray should not be red
        gray_rgb = hex_to_rgb(result.achromatopsia)
        assert gray_rgb.r == gray_rgb.g == gray_rgb.b


# =============================================================================
# Color info
# =============================================================================
class TestColorInfo:
    def test_get_color_info(self) -> None:
        info = get_color_info("FF6B35")
        assert isinstance(info, ColorInfo)
        assert info.hex == "FF6B35"
        assert isinstance(info.rgb, RGB)
        assert isinstance(info.hsl, HSL)
        assert isinstance(info.hsv, HSV)
        assert isinstance(info.cmyk, CMYK)
        assert isinstance(info.oklch, OKLCH)
        assert isinstance(info.is_light, bool)
        assert isinstance(info.is_warm, bool)

    def test_with_hash(self) -> None:
        info = get_color_info("#3498DB")
        assert info.hex == "3498DB"


# =============================================================================
# Types exported
# =============================================================================
class TestExports:
    def test_all_types(self) -> None:
        """All public types are importable from colorfyi."""
        assert RGB is not None
        assert HSL is not None
        assert HSV is not None
        assert CMYK is not None
        assert OKLCH is not None
        assert Lab is not None
        assert ContrastResult is not None
        assert ShadeStep is not None
        assert ColorInfo is not None
        assert HarmonySet is not None
        assert ColorBlindResult is not None
        assert CompareResult is not None


# =============================================================================
# Edge cases
# =============================================================================
class TestEdgeCases:
    def test_hex_with_hash(self) -> None:
        rgb = hex_to_rgb("#FF0000")
        assert rgb == RGB(255, 0, 0)

    def test_hex_lowercase(self) -> None:
        rgb = hex_to_rgb("ff6b35")
        assert rgb.r == 255

    def test_lightness_scale_steps_1(self) -> None:
        result = lightness_scale("FF0000", steps=1)
        assert len(result) == 1

    def test_saturation_scale_steps_1(self) -> None:
        result = saturation_scale("FF0000", steps=1)
        assert len(result) == 1

    def test_hue_shift_scale_steps_0(self) -> None:
        result = hue_shift_scale("FF0000", steps=0)
        assert result == []

    def test_gradient_steps_2(self) -> None:
        result = gradient_steps("FF0000", "0000FF", steps=2)
        assert len(result) == 2

    def test_mix_ratio_0(self) -> None:
        result = mix_colors("FF0000", "0000FF", ratio=0.0)
        assert result.upper().startswith("F")  # close to red

    def test_mix_ratio_1(self) -> None:
        result = mix_colors("FF0000", "0000FF", ratio=1.0)
        assert result.upper().startswith("0")  # close to blue

    def test_monochromatic_count_1(self) -> None:
        result = monochromatic("FF0000", count=1)
        assert len(result) == 1

    def test_contrast_same_color(self) -> None:
        result = contrast_ratio("FFFFFF", "FFFFFF")
        assert result.ratio == 1.0
        assert result.aa_normal is False

    def test_pure_black(self) -> None:
        info = get_color_info("000000")
        assert info.is_light is False
        assert info.rgb == RGB(0, 0, 0)

    def test_pure_white(self) -> None:
        info = get_color_info("FFFFFF")
        assert info.is_light is True
        assert info.rgb == RGB(255, 255, 255)

    def test_blindness_grayscale(self) -> None:
        result = simulate_color_blindness("808080")
        assert result.original == "808080"
