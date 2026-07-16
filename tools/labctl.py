#!/usr/bin/env python3
"""labctl — small stdlib CLI for Grok-Workspace-main.

No third-party deps. Coordinates journal/seeds with GRMC when available.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRMC = ROOT / "experiments" / "grmc"
LAB_DATA = ROOT / ".lab_data" / "grmc"
JOURNAL = ROOT / "journal"
SEEDS = ROOT / "seeds"
EXPERIMENTS = ROOT / "experiments"
TEMPLATES = ROOT / "templates"


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sections_from_md(path: Path) -> list[tuple[str, str]]:
    """Parse ## headings into (title, body) pairs; skip empty bodies."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^##\s+", text)
    out: list[tuple[str, str]] = []
    for part in parts[1:]:
        lines = part.strip().splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        if not body:
            continue
        # skip pure checklist-only noise if no prose? keep all non-empty
        out.append((title, body))
    return out


def cmd_status(_: argparse.Namespace) -> int:
    print(f"Lab root: {ROOT}")
    print(f"GRMC path: {GRMC}  exists={GRMC.exists()}")
    print(f"Lab data:  {LAB_DATA}")
    print()
    print("Journal:")
    for name in ("inbox.md", "open_questions.md", "decisions.md", "self_model.md"):
        p = JOURNAL / name
        n = len(_sections_from_md(p)) if p.exists() else 0
        print(f"  {name:20} sections_with_body={n}  exists={p.exists()}")
    seeds = list(SEEDS.glob("*.md")) if SEEDS.exists() else []
    print(f"Seeds: {len(seeds)} file(s)")
    print()
    if (GRMC / ".git").exists() or (GRMC / ".git").is_file():
        try:
            log = subprocess.check_output(
                ["git", "-C", str(GRMC), "log", "-1", "--oneline"],
                text=True,
            ).strip()
            print(f"GRMC HEAD: {log}")
        except subprocess.CalledProcessError:
            print("GRMC: git log failed")
    else:
        print("GRMC missing — run: make setup")
        return 1

    LAB_DATA.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["grmc", "status", "--data-dir", str(LAB_DATA)],
            cwd=str(GRMC),
            check=False,
        )
    except FileNotFoundError:
        print("(grmc not on PATH — pip install -e experiments/grmc)")
    return 0


def cmd_inbox_add(args: argparse.Namespace) -> int:
    inbox = JOURNAL / "inbox.md"
    inbox.parent.mkdir(parents=True, exist_ok=True)
    if not inbox.exists():
        inbox.write_text("# Inbox → GRMC\n\n", encoding="utf-8")
    title = args.title.strip()
    body = args.body.strip() if args.body else ""
    if not body and not sys.stdin.isatty():
        body = sys.stdin.read().strip()
    if not body:
        print("error: provide --body or pipe text", file=sys.stderr)
        return 2
    block = f"\n## {title}\n\n{body}\n"
    with inbox.open("a", encoding="utf-8") as fh:
        fh.write(block)
    print(f"✓ appended to journal/inbox.md: {title}")
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    log_dir = JOURNAL / "log"
    log_dir.mkdir(parents=True, exist_ok=True)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = log_dir / f"{day}.md"
    if not path.exists():
        path.write_text(f"# Session log {day}\n\n", encoding="utf-8")
    entry = args.text.strip()
    if not entry and not sys.stdin.isatty():
        entry = sys.stdin.read().strip()
    if not entry:
        print(f"log file: {path}")
        print(path.read_text(encoding="utf-8")[-2000:])
        return 0
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"\n## {_utc_now()}\n\n{entry}\n")
    print(f"✓ logged → {path}")
    return 0


def _grmc_ingest(text: str, source: str, concepts: str) -> None:
    LAB_DATA.mkdir(parents=True, exist_ok=True)
    cmd = [
        "grmc",
        "ingest",
        "--text",
        text,
        "--source",
        source,
        "--embedder",
        "hashing",
        "--data-dir",
        str(LAB_DATA),
    ]
    if concepts:
        cmd.extend(["--concepts", concepts])
    subprocess.run(cmd, cwd=str(GRMC), check=True)


def cmd_seed_grmc(args: argparse.Namespace) -> int:
    if not GRMC.exists():
        print("error: GRMC missing — make setup", file=sys.stderr)
        return 1

    items: list[tuple[str, str, str, str]] = []
    # (title, body, source, concepts)

    if args.seeds or args.all:
        for path in sorted(SEEDS.glob("*.md")):
            for title, body in _sections_from_md(path):
                text = f"[{path.stem}] {title}\n{body}"
                items.append((title, text, f"seed:{path.stem}", "lab,seed"))

    if args.inbox or args.all:
        for title, body in _sections_from_md(JOURNAL / "inbox.md"):
            text = f"[inbox] {title}\n{body}"
            items.append((title, text, "journal:inbox", "lab,inbox"))

    if args.self_model or args.all:
        for title, body in _sections_from_md(JOURNAL / "self_model.md"):
            text = f"[self_model] {title}\n{body}"
            items.append((title, text, "journal:self_model", "self_model,lab"))

    if not items:
        print("nothing to ingest (use --inbox / --seeds / --self-model / --all)")
        return 0

    print(f"Ingesting {len(items)} episode(s) → {LAB_DATA}")
    for title, text, source, concepts in items:
        try:
            _grmc_ingest(text[:8000], source, concepts)
            print(f"  ✓ {title[:60]}")
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            print(f"  ✗ {title}: {exc}", file=sys.stderr)
            return 1

    if args.reflect:
        print("→ grmc reflect")
        subprocess.run(
            [
                "grmc",
                "reflect",
                "--embedder",
                "hashing",
                "--data-dir",
                str(LAB_DATA),
            ],
            cwd=str(GRMC),
            check=False,
        )
    print("Done. Review: grmc propose  (graph write still needs approve)")
    return 0


def cmd_new_experiment(args: argparse.Namespace) -> int:
    name = re.sub(r"[^a-zA-Z0-9._-]+", "-", args.name.strip()).strip("-").lower()
    if not name:
        print("error: invalid name", file=sys.stderr)
        return 2
    dest = EXPERIMENTS / name
    if dest.exists():
        print(f"error: already exists: {dest}", file=sys.stderr)
        return 1
    dest.mkdir(parents=True)
    (dest / "notes").mkdir()
    tpl = (TEMPLATES / "experiment_README.md").read_text(encoding="utf-8")
    (dest / "README.md").write_text(
        tpl.replace("{{NAME}}", name),
        encoding="utf-8",
    )
    # index line
    idx = EXPERIMENTS / "README.md"
    if idx.exists():
        with idx.open("a", encoding="utf-8") as fh:
            fh.write(
                f"\n| {name} | `experiments/{name}/` | local | idea |\n"
            )
    print(f"✓ created experiments/{name}/")
    print(f"  edit experiments/{name}/README.md")
    return 0


def cmd_doctor(_: argparse.Namespace) -> int:
    ok = True
    checks = [
        ("lab README", (ROOT / "README.md").exists()),
        ("AGENTS.md", (ROOT / "AGENTS.md").exists()),
        ("journal/inbox.md", (JOURNAL / "inbox.md").exists()),
        ("GRMC checkout", GRMC.exists()),
        ("GRMC pyproject", (GRMC / "pyproject.toml").exists()),
    ]
    for label, passed in checks:
        mark = "✓" if passed else "✗"
        print(f"  {mark} {label}")
        ok = ok and passed
    # grmc binary
    try:
        subprocess.run(["grmc", "--help"], capture_output=True, check=True)
        print("  ✓ grmc on PATH")
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("  · grmc not installed (optional until install-grmc)")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="labctl",
        description="Grok lab control (stdlib). Coordinates journal ↔ GRMC.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("status", help="Lab + GRMC dashboard")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("doctor", help="Sanity checks")
    p.set_defaults(func=cmd_doctor)

    p = sub.add_parser("inbox-add", help="Append a section to journal/inbox.md")
    p.add_argument("--title", "-t", required=True)
    p.add_argument("--body", "-b", default="")
    p.set_defaults(func=cmd_inbox_add)

    p = sub.add_parser("log", help="Append to today's session log (or show it)")
    p.add_argument("text", nargs="?", default="")
    p.set_defaults(func=cmd_log)

    p = sub.add_parser(
        "seed-grmc",
        help="Ingest seeds/inbox/self_model sections into GRMC (hashing embedder)",
    )
    p.add_argument("--all", action="store_true", help="seeds + inbox + self_model")
    p.add_argument("--seeds", action="store_true")
    p.add_argument("--inbox", action="store_true")
    p.add_argument("--self-model", action="store_true")
    p.add_argument(
        "--reflect",
        action="store_true",
        help="Run grmc reflect after ingest (still no graph write)",
    )
    p.set_defaults(func=cmd_seed_grmc)

    p = sub.add_parser("new-experiment", help="Scaffold experiments/<name>/")
    p.add_argument("name")
    p.set_defaults(func=cmd_new_experiment)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
