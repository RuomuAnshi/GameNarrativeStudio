# Game Narrative Studio

A local-first Cursor / Codex writing and localization toolkit for **Ren'Py**, **WebGAL**, and **Paradox** games.

## Project status
- Shared agents and 10 workflow skills (character voice, dialogue editing, narrative continuity, QA, localization).
- Conservative adapters for Ren'Py `translate strings`, WebGAL simple dialogue lines, and Paradox `l_english`-style YAML with BOM.
- Dependency-free JSON scene validation and sample Ren'Py export.
- **Limited scope**: not a complete engine parser or guaranteed in-game compatibility.
- The WebGAL scene-authoring workflow is developed separately at [RuomuAnshi/webgal-author](https://github.com/RuomuAnshi/webgal-author) (MIT). Use it for scene generation and resource scanning; this project only supplies conservative localization patches.

## Run
```bash
python -m unittest discover -s tests -v
python tools/narrative.py validate scenes/demo.json
python tools/narrative.py export-renpy scenes/demo.json exports/demo.rpy
python tools/format_adapters.py renpy examples/renpy_source.rpy examples/renpy_changes.json exports/renpy_out.rpy
python tools/format_adapters.py webgal examples/webgal_source.txt examples/webgal_changes.json exports/webgal_out.txt
python tools/format_adapters.py paradox examples/paradox_source_l_english.yml examples/paradox_changes.json exports/paradox_out.yml
```

See `AGENTS.md` and `.agents/skills/` for usage. Third-party skills are **not vendored** by default. This repository does not bypass model content restrictions.

## Attribution
WebGAL source workflow: https://github.com/RuomuAnshi/webgal-author (MIT). Original tool code in this repo is separately maintained.
