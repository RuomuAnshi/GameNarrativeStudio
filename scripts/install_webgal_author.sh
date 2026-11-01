#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="$root/.agents/skills/webgal-author"
if [ -e "$target" ]; then echo "Already exists: $target"; exit 1; fi
git clone --depth 1 https://github.com/RuomuAnshi/webgal-author.git "$target"
echo "Installed upstream WebGAL author to $target. Review license and files before use."
