# Game Narrative Studio — Cursor / Codex
Read `project.json`, character cards and relevant scene before editing.
Select the most specific skill in `.agents/skills/`. For new WebGAL scene authoring, install and read [webgal-author](https://github.com/RuomuAnshi/webgal-author); its source is not copied here.

Rules:
- Preserve characters' distinct voices; avoid overexplaining feelings, generic sentiment, formulaic resolutions, and unsourced canon.
- For mature content, document ages and project rating; follow the model's content policy.
- Never overwrite game originals. Patch allowlisted strings only and preserve keys, tokens, control codes, encoding and whitespace.
- After edits run `python -m unittest discover -s tests -v`; do not claim real engine validation without executing the engine.
- Work locally; no cloud API is required by scripts.
