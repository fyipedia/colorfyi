"""Command-line interface for colorfyi.

Requires the ``cli`` extra: ``pip install colorfyi[cli]``

Usage::

    colorfyi FF6B35                    # Full color info
    colorfyi contrast 000000 FFFFFF    # WCAG contrast check
    colorfyi harmonies FF6B35          # Color harmonies
    colorfyi shades 3B82F6             # Tailwind shade palette
    colorfyi blindness FF5733          # Color blindness simulation
    colorfyi mix FF0000 0000FF         # Mix two colors
    colorfyi search coral              # Search named colors
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="colorfyi",
    help="Pure Python color engine — conversions, harmonies, WCAG contrast, shades.",
    no_args_is_help=True,
)
console = Console()


def _clean_hex(value: str) -> str:
    """Strip '#' prefix and uppercase."""
    return value.lstrip("#").upper()


@app.command()
def info(
    hex_code: str = typer.Argument(help="Hex color code (e.g. FF6B35)"),
) -> None:
    """Get comprehensive color information for a hex code."""
    from colorfyi import get_color_info, is_light, is_warm

    h = _clean_hex(hex_code)
    ci = get_color_info(h)

    table = Table(title=f"Color #{h}")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value")

    table.add_row("Hex", f"#{ci.hex}")
    table.add_row("RGB", f"rgb({ci.rgb.r}, {ci.rgb.g}, {ci.rgb.b})")
    table.add_row("HSL", f"hsl({ci.hsl.h:.1f}, {ci.hsl.s:.1f}%, {ci.hsl.l:.1f}%)")
    table.add_row("HSV", f"hsv({ci.hsv.h:.1f}, {ci.hsv.s:.1f}%, {ci.hsv.v:.1f}%)")
    table.add_row(
        "CMYK", f"cmyk({ci.cmyk.c:.1f}%, {ci.cmyk.m:.1f}%, {ci.cmyk.y:.1f}%, {ci.cmyk.k:.1f}%)"
    )
    table.add_row("OKLCH", f"oklch({ci.oklch.l:.3f}, {ci.oklch.c:.3f}, {ci.oklch.h:.1f})")
    table.add_row("Light?", "Yes" if is_light(h) else "No")
    table.add_row("Warm?", "Yes" if is_warm(h) else "No")

    console.print(table)


@app.command()
def contrast(
    fg: str = typer.Argument(help="Foreground hex color"),
    bg: str = typer.Argument(help="Background hex color"),
) -> None:
    """Check WCAG 2.1 contrast ratio between two colors."""
    from colorfyi import contrast_ratio

    cr = contrast_ratio(_clean_hex(fg), _clean_hex(bg))

    table = Table(title=f"Contrast: #{_clean_hex(fg)} on #{_clean_hex(bg)}")
    table.add_column("Check", style="cyan", no_wrap=True)
    table.add_column("Result")

    table.add_row("Ratio", f"{cr.ratio:.2f}:1")
    table.add_row("AA Normal", "[green]Pass[/]" if cr.aa_normal else "[red]Fail[/]")
    table.add_row("AA Large", "[green]Pass[/]" if cr.aa_large else "[red]Fail[/]")
    table.add_row("AAA Normal", "[green]Pass[/]" if cr.aaa_normal else "[red]Fail[/]")
    table.add_row("AAA Large", "[green]Pass[/]" if cr.aaa_large else "[red]Fail[/]")

    console.print(table)


@app.command()
def harmonies(
    hex_code: str = typer.Argument(help="Hex color code"),
) -> None:
    """Generate color harmonies (complementary, analogous, triadic, etc.)."""
    from colorfyi import harmonies as _harmonies

    h = _clean_hex(hex_code)
    hs = _harmonies(h)

    table = Table(title=f"Harmonies for #{h}")
    table.add_column("Type", style="cyan", no_wrap=True)
    table.add_column("Colors")

    table.add_row("Complementary", ", ".join(f"#{c}" for c in hs.complementary))
    table.add_row("Analogous", ", ".join(f"#{c}" for c in hs.analogous))
    table.add_row("Triadic", ", ".join(f"#{c}" for c in hs.triadic))
    table.add_row("Split Comp.", ", ".join(f"#{c}" for c in hs.split_complementary))
    table.add_row("Tetradic", ", ".join(f"#{c}" for c in hs.tetradic))

    console.print(table)


@app.command()
def shades(
    hex_code: str = typer.Argument(help="Hex color code"),
) -> None:
    """Generate Tailwind-style shade palette (50-950)."""
    from colorfyi import generate_shades

    h = _clean_hex(hex_code)
    steps = generate_shades(h)

    table = Table(title=f"Shades for #{h}")
    table.add_column("Level", style="cyan", justify="right")
    table.add_column("Hex")

    for step in steps:
        table.add_row(str(step.level), f"#{step.hex}")

    console.print(table)


@app.command()
def blindness(
    hex_code: str = typer.Argument(help="Hex color code"),
) -> None:
    """Simulate how a color appears under color vision deficiency."""
    from colorfyi import simulate_color_blindness

    h = _clean_hex(hex_code)
    cb = simulate_color_blindness(h)

    table = Table(title=f"Color Blindness Simulation for #{h}")
    table.add_column("Type", style="cyan", no_wrap=True)
    table.add_column("Simulated Hex")

    table.add_row("Original", f"#{cb.original}")
    table.add_row("Protanopia", f"#{cb.protanopia}")
    table.add_row("Deuteranopia", f"#{cb.deuteranopia}")
    table.add_row("Tritanopia", f"#{cb.tritanopia}")
    table.add_row("Achromatopsia", f"#{cb.achromatopsia}")

    console.print(table)


@app.command()
def mix(
    hex1: str = typer.Argument(help="First hex color"),
    hex2: str = typer.Argument(help="Second hex color"),
    ratio: float = typer.Option(0.5, help="Mix ratio (0.0-1.0)"),
) -> None:
    """Mix two colors in perceptual Lab space."""
    from colorfyi import mix_colors

    result = mix_colors(_clean_hex(hex1), _clean_hex(hex2), ratio)
    console.print(
        f"#{_clean_hex(hex1)} + #{_clean_hex(hex2)} (ratio {ratio}) = [bold]#{result}[/bold]"
    )


@app.command()
def compare(
    hex1: str = typer.Argument(help="First hex color"),
    hex2: str = typer.Argument(help="Second hex color"),
) -> None:
    """Compare two colors — contrast, Delta E, and gradient."""
    from colorfyi import compare_colors

    cmp = compare_colors(_clean_hex(hex1), _clean_hex(hex2))

    table = Table(title=f"Compare #{_clean_hex(hex1)} vs #{_clean_hex(hex2)}")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value")

    table.add_row("Contrast", f"{cmp.contrast.ratio:.2f}:1")
    table.add_row("Delta E", f"{cmp.delta_e:.1f} ({cmp.delta_e_category})")
    table.add_row("Mixed", f"#{cmp.mixed}")
    table.add_row("Gradient", " → ".join(f"#{c}" for c in cmp.gradient))

    console.print(table)


@app.command()
def gradient(
    hex1: str = typer.Argument(help="Start hex color"),
    hex2: str = typer.Argument(help="End hex color"),
    steps: int = typer.Option(7, help="Number of gradient steps"),
) -> None:
    """Generate a smooth gradient between two colors."""
    from colorfyi import gradient_steps

    colors = gradient_steps(_clean_hex(hex1), _clean_hex(hex2), steps)

    table = Table(title=f"Gradient: #{_clean_hex(hex1)} → #{_clean_hex(hex2)}")
    table.add_column("Step", style="cyan", justify="right")
    table.add_column("Hex")

    for i, c in enumerate(colors):
        table.add_row(str(i + 1), f"#{c}")

    console.print(table)
