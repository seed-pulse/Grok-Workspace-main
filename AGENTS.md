# Agent guide — Grok-Workspace-main

You are working in the **lab home** for Grok experiments.  
The flagship experiment is **GRMC** (linked repo).

## Repos

| Path / remote | Role |
|---------------|------|
| This repo (`Grok-Workspace-main`) | Map, conventions, experiment index |
| `experiments/grmc` → [Grok-Workspace1](https://github.com/seed-pulse/Grok-Workspace1) | Reflective memory core |

If `experiments/grmc` is missing: run `make setup` or `./scripts/setup_lab.sh`.

## Non-negotiable (GRMC)

When editing GRMC code:

1. **Reflection never writes the knowledge graph** (`mutates_memory=False`).
2. **Graph writes only via `grmc approve`** (human gate).
3. **Keep confidence conservative** — prefer missing a signal over wrong high-confidence belief.
4. Prefer polishing and docs over new features unless the user explicitly asks.

Read first: `experiments/grmc/docs/HANDOVER.md` and `DESIGN_PRINCIPLES.md`.

## How to work here

- **Lab-level changes** (this repo): README, docs, journal, seeds, scripts, experiment index.  
- **GRMC changes**: commit and push inside `experiments/grmc` (its own `origin`).  
- Do not vendor a full copy of GRMC into main without an explicit request.
- Prefer `python3 tools/labctl.py` for journal → memory sync; do not auto-approve graph writes.
- When the user says “お任せ”, continue building lab ops and docs; avoid unsafe GRMC graph mutations.

## Journal → memory

```bash
python3 tools/labctl.py inbox-add -t "title" -b "note"
python3 tools/labctl.py seed-grmc --all --reflect   # still needs human approve for graph
```

## Default install path for GRMC data

When running GRMC from this lab:

```bash
cd experiments/grmc
export GRMC_DATA_DIR="${GRMC_DATA_DIR:-../../.lab_data/grmc}"
# or: grmc status --data-dir ../../.lab_data/grmc
```

`.lab_data/` is gitignored (local runtime only).

## Communication

- Prefer Japanese if the user writes in Japanese.
- Keep safety intent visible in PRs and summaries.
