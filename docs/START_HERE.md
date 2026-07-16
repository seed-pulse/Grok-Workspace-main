# Start here

Welcome to **Grok-Workspace-main**.

## 1. Get GRMC

```bash
# from repo root
make setup
cd experiments/grmc
pip install -e ".[dev]"
```

## 2. Smoke check

```bash
pytest -q
grmc status --data-dir ../../.lab_data/grmc
```

Create the data dir if needed:

```bash
mkdir -p ../../.lab_data/grmc
grmc ingest -t "ラボ開始メモ" -c "lab,grmc" --embedder hashing --data-dir ../../.lab_data/grmc
grmc reflect --embedder hashing --data-dir ../../.lab_data/grmc
```

## 3. Read the intent

| Doc | Why |
|-----|-----|
| [LAB_MAP.md](LAB_MAP.md) | How main ↔ GRMC fit together |
| GRMC `docs/HANDOVER.md` | How to continue the memory experiment |
| GRMC `docs/DESIGN_PRINCIPLES.md` | Safety principles |
| GRMC `docs/QUICKSTART.md` | Day-to-day GRMC commands |

## 4. Loop to remember

```
ingest → reflect (think only) → propose → approve (write) → inspect
```

If you only remember one rule: **reflection does not write the graph.**
