---
name: webgal-localization
description: Localize simple WebGAL dialogue without modifying commands; defer scene authoring to webgal-author.
---
# WebGAL localization
For simple dialogue patches use `tools/format_adapters.py webgal` with exact line keys. Protect commands, delimiters and variables. For richer scripts, resource scanning and scene creation, use upstream `RuomuAnshi/webgal-author` rather than pretending this lightweight patcher parses the full format. Run real parser validation separately.
