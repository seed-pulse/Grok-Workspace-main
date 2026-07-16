# Lab map

## Two repositories

```
┌─────────────────────────────────────┐
│  Grok-Workspace-main                │
│  入口・地図・規約・experiments/     │
│                                     │
│   experiments/grmc  ──clone──►      │
└──────────────────│──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│  Grok-Workspace1 (GRMC)             │
│  長期記憶・反省・承認・グラフ       │
│  v0.8.1 stable experiment stop      │
└─────────────────────────────────────┘
```

## Responsibility split

| Concern | Where |
|---------|--------|
| “What experiments exist?” | main `experiments/README.md` |
| “How do agents behave?” | main `AGENTS.md` |
| Memory implementation | GRMC repo |
| Safety of graph writes | GRMC approval queue |
| Dual-Grok file bridge | GRMC `grmc bridge` |

## Data

- **Code:** git  
- **Runtime memory:** prefer `.lab_data/grmc` under main (gitignored), or GRMC’s own `./grmc_data`  

Do not commit SQLite / Chroma blobs unless explicitly requested.

## Adding a new experiment

1. Create `experiments/<name>/` (own mini-README).  
2. List it in `experiments/README.md`.  
3. Link from main README if it is long-lived.  
4. Keep GRMC safety rules if the experiment touches memory/graph ideas.
