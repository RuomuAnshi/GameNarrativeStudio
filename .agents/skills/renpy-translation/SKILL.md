---
name: renpy-translation
description: Modify official Ren'Py translate strings files without breaking interpolation.
---
# Ren'Py translation
Only apply `tools/format_adapters.py renpy` to generated `translate LANGUAGE strings:` blocks. Keep original `old` keys, text tags, substitutions and escapes. Script translation blocks require a separate implementation. Verify output in Ren'Py before release.
