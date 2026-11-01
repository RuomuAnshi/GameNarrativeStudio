# WebGAL integration
Upstream: https://github.com/RuomuAnshi/webgal-author (MIT, copyright PjShelter, 2026).

For **new scene generation**, use upstream `webgal-author`: sniff plain/Markdown input, scan `public/game/` assets, segment scenes, compose AST and render. Consult its `SKILL.md`, `references/command-spec.md`, and `tools/validate-scene.ts`. Validate using a **real compatible WebGAL parser** when available; local line checks are not sufficient.

For **localization of an existing scene**, use the conservative `tools/format_adapters.py webgal` adapter. It only targets a simple dialogue at a supplied line number, leaving commands untouched. Complex inline directives, choices, expressions, and asset command edits require upstream tooling or manual review.

The installer `scripts/install_webgal_author.sh` fetches the upstream repository independently. No upstream code is vendored here. The README of upstream refers to another owner in its sample clone command; use the actual `RuomuAnshi/webgal-author` repository URL.
