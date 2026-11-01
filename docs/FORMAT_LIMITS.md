# Format support and known limitations

| Engine | Currently supported | Not supported |
| --- | --- | --- |
| Ren'Py | generated `translate language strings` pairs | all script translation blocks and expressions |
| WebGAL | simple speaker:dialogue lines keyed by original 1-based line number | compound commands, escaped semicolons, scene AST; use upstream webgal-author |
| Paradox | UTF-8 BOM `l_english:`-style entries with `KEY:0 "text"` | all title-specific syntax and runtime formatting |
| JSON | allowlisted `lines[].text` with protected tokens | arbitrary game assets |

The adapters do not call an AI model or modify game files in place. CI verifies sample fixtures, not real in-engine execution. Review every resulting diff.
