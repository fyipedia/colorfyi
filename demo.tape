# colorfyi — Python Color Science Library Demo
Output demo.gif

Set FontSize 20
Set Width 1000
Set Height 580
Set Shell "zsh"
Set Theme "Catppuccin Mocha"
Set TypingSpeed 30ms
Set Padding 24

Type "uv run --with colorfyi python3"
Enter
Sleep 2.5s

Type "from colorfyi import hex_to_rgb, contrast_ratio, color_info"
Enter
Sleep 1s

Type "# Convert hex to RGB"
Enter
Sleep 0.5s

Type "hex_to_rgb('FF6B35')"
Enter
Sleep 1.5s

Type "# WCAG contrast ratio"
Enter
Sleep 0.5s

Type "contrast_ratio('FF6B35', 'FFFFFF')"
Enter
Sleep 1.5s

Type "# Full color info"
Enter
Sleep 0.5s

Type "color_info('FF6B35')['name']"
Enter
Sleep 2s

Type "exit()"
Enter
Sleep 1s
