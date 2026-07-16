#!/usr/bin/env bash
# Clone GRMC into experiments/grmc if missing.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="$ROOT/experiments/grmc"
REMOTE="${GRMC_REMOTE:-https://github.com/seed-pulse/Grok-Workspace1.git}"

mkdir -p "$ROOT/experiments"
mkdir -p "$ROOT/.lab_data/grmc"

if [[ -d "$TARGET/.git" ]]; then
  echo "✓ GRMC already present: $TARGET"
  git -C "$TARGET" remote -v | head -2
  exit 0
fi

if [[ -e "$TARGET" ]]; then
  echo "error: $TARGET exists but is not a git repo" >&2
  exit 1
fi

echo "→ Cloning GRMC into experiments/grmc"
git clone "$REMOTE" "$TARGET"
echo "✓ Done. Next:"
echo "  cd experiments/grmc && pip install -e '.[dev]' && pytest -q"
echo "  grmc status --data-dir ../../.lab_data/grmc"
