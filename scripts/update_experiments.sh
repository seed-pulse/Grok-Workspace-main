#!/usr/bin/env bash
# Pull latest GRMC (and future experiment clones).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

update_one() {
  local dir="$1"
  if [[ -d "$dir/.git" ]]; then
    echo "→ updating $dir"
    git -C "$dir" pull --ff-only || git -C "$dir" pull --rebase
  else
    echo "· skip (not a git clone): $dir"
  fi
}

update_one "$ROOT/experiments/grmc"

# Future: for d in "$ROOT/experiments"/*; do update_one "$d"; done
echo "✓ update pass complete"
