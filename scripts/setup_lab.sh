#!/usr/bin/env bash
# Ensure GRMC submodule (or clone) is present under experiments/grmc.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="$ROOT/experiments/grmc"
REMOTE="${GRMC_REMOTE:-https://github.com/seed-pulse/Grok-Workspace1.git}"

mkdir -p "$ROOT/experiments"
mkdir -p "$ROOT/.lab_data/grmc"

# Prefer git submodule when .gitmodules is present
if [[ -f "$ROOT/.gitmodules" ]] && grep -q "experiments/grmc" "$ROOT/.gitmodules"; then
  echo "→ Initializing submodule experiments/grmc"
  git -C "$ROOT" submodule update --init --recursive
  if [[ -d "$TARGET/.git" || -f "$TARGET/.git" ]]; then
    echo "✓ GRMC submodule ready: $TARGET"
    git -C "$TARGET" log -1 --oneline
    exit 0
  fi
fi

if [[ -d "$TARGET/.git" ]]; then
  echo "✓ GRMC already present: $TARGET"
  git -C "$TARGET" log -1 --oneline
  exit 0
fi

if [[ -e "$TARGET" ]]; then
  echo "error: $TARGET exists but is not a git checkout" >&2
  exit 1
fi

echo "→ Cloning GRMC into experiments/grmc"
git clone "$REMOTE" "$TARGET"
echo "✓ Done."
echo "  cd experiments/grmc && pip install -e '.[dev]'"
echo "  grmc status --data-dir ../../.lab_data/grmc"
