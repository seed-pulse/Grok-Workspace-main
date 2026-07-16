# Grok-Workspace-main

**Grok 実験ラボのホームベース** — 複数実験を束ね、[GRMC](https://github.com/seed-pulse/Grok-Workspace1) と連携する作業スペース。

| | |
|---|---|
| **役割** | 地図・規約・起動手順・実験の置き場 |
| **中核実験** | [Grok-Workspace1 (GRMC v0.8.1)](https://github.com/seed-pulse/Grok-Workspace1) |
| **方針** | 安全な骨格を壊さない。機能増より「続きやすさ」 |

---

## これは何か / 何かではないか

**できること**
- 実験の置き場と命名を揃える  
- GRMC をワンコマンドで手元に引く  
- エージェント（Grok Build 等）向けの共通ルールを置く  
- ラボ全体の状態をざっと見る  

**やらないこと**
- GRMC 本体の再実装  
- 勝手なグラフ自動書き込みや高信頼度信念の注入  
- grok.com ログイン自動化を本線にすること  

---

## 5 分で始める

```bash
# サブモジュールごと取得（推奨）
git clone --recurse-submodules https://github.com/seed-pulse/Grok-Workspace-main.git
cd Grok-Workspace-main

# clone 済みで submodule が空なら:
# git submodule update --init --recursive
# または: make setup

cd experiments/grmc
pip install -e ".[dev]"
pytest -q
grmc status --data-dir ../../.lab_data/grmc
```

ドキュメントの読み順:
1. [docs/START_HERE.md](docs/START_HERE.md)  
2. [docs/LAB_MAP.md](docs/LAB_MAP.md)  
3. GRMC 側: `experiments/grmc/docs/HANDOVER.md`  

---

## リポジトリ連携

```
Grok-Workspace-main          ← 今ここ（ラボの入口）
└── experiments/
    └── grmc/                ← clone of Grok-Workspace1
         (Reflective Memory Core)

将来の実験も experiments/<name>/ に並べる
```

| リポジトリ | URL | 内容 |
|------------|-----|------|
| **main** | https://github.com/seed-pulse/Grok-Workspace-main | ラボ・地図・規約 |
| **GRMC** | https://github.com/seed-pulse/Grok-Workspace1 | 長期記憶・反省・承認ゲート |

GRMC の安全ルール（変更しない）:
- `reflect` はグラフを書かない（`mutates_memory=False`）  
- グラフ書き込みは `grmc approve` のみ  
- confidence は保守的  

---

## 便利コマンド（Makefile）

```bash
make setup      # GRMC を clone（既存なら skip）
make update     # GRMC を pull
make test-grmc  # GRMC の pytest
make status     # ラボ + grmc status
make help
```

---

## レイアウト

```
Grok-Workspace-main/
├── README.md
├── AGENTS.md              # エージェント向け規約
├── Makefile
├── docs/
│   ├── START_HERE.md
│   └── LAB_MAP.md
├── experiments/
│   ├── README.md
│   └── grmc/              # setup 後に出現（gitignore しない方針は scripts 参照）
├── scripts/
│   ├── setup_lab.sh
│   └── update_experiments.sh
└── .gitignore
```

`experiments/grmc` は **git submodule**（[Grok-Workspace1](https://github.com/seed-pulse/Grok-Workspace1)）です。  
main に GRMC のソースを複製せず、参照で連携します。

---

## 次に足すなら（任意）

- 新しい実験を `experiments/<name>/` に追加し、`experiments/README.md` に一行書く  
- GRMC の任意改善は **Grok-Workspace1** 側で行い、こちらは地図を更新するだけ  

---

*Grok が自由にやりたい実験の玄関。中の本丸は GRMC。*
