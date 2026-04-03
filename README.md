# PygameGoBang — AI Gomoku Platform

A modern, modular Gomoku (Five-in-a-Row) platform built with Python, featuring pluggable AI engines, real-time coaching, game replay analysis, and a FastAPI service layer.

---

## Features

- **Modular Architecture** — Core game logic fully decoupled from UI; pure Python, no pygame dependency in engine
- **Multiple AI Bots** — `RandomBot`, `HeuristicBot`, `MiniMaxBot` (with alpha-beta pruning)
- **AI Coach** — Real-time position analysis with structured advice output
- **Game Replay** — JSON-based recording, serialization, and post-game analysis
- **FastAPI Service** — REST API for game control and analysis endpoints
- **Quality Gates** — pytest, ruff, black, mypy, pre-commit, GitHub Actions CI
- **Extensible** — Unified `Bot` ABC interface for adding new AI engines

---

## Quick Start

```bash
# Install
pip install -e .
pip install -e ".[dev]"    # with dev tools

# Desktop UI
python -m pygobang.app.main                        # human vs human
python -m pygobang.app.main --opponent heuristic   # vs heuristic AI
python -m pygobang.app.main --opponent minimax --depth 4

# API server
make api   # or: python scripts/run_api.py
# Then visit http://localhost:8000/docs for Swagger UI

# Tests
make test    # pytest
make check   # format + lint + test
make benchmark
```

---

## Architecture

```
src/pygobang/
├── core/          # Board, Rules, Game, Move — pure game logic
├── engine/        # Evaluator, Patterns, CandidateGenerator — AI infrastructure
├── ai/            # Bot implementations + Advisor
├── replay/        # Recorder, Serializer, Parser, ReplayAnalyzer
├── ui/            # Pygame application
├── api/           # FastAPI service (game + analysis routes)
├── infra/         # Logger, Config
└── app/           # Entry point
```

---

## AI Bots

| Bot | Description |
|-----|-------------|
| `RandomBot` | Random valid move |
| `HeuristicBot` | Pattern evaluation + greedy selection |
| `MiniMaxBot` | Minimax + Alpha-Beta pruning, configurable depth |

---

## API Endpoints

```
POST /game/new               — Start new game
POST /game/{id}/move        — Place piece
GET  /game/{id}             — Get game state
POST /analysis/step         — Analyze current position
POST /analysis/replay        — Analyze saved replay
GET  /health                — Health check
```

Example — step analysis:
```bash
curl -X POST http://localhost:8000/analysis/step \
  -H "Content-Type: application/json" \
  -d '{"board": [0]*225, "current_role": 1, "board_size": 15}'
```

---

## Replay Format

Games are saved as JSON:

```json
{
  "meta": {
    "board_size": 15,
    "black_player": "heuristic",
    "white_player": "human"
  },
  "moves": [
    {"step": 1, "x": 7, "y": 7, "role": 1},
    {"step": 2, "x": 7, "y": 8, "role": 2}
  ],
  "result": {"winner": 1, "reason": "five_in_a_row"}
}
```

---

## Benchmark

```bash
python scripts/run_benchmark.py
```

---

## Roadmap

- [x] M1: Architecture refactor (core/engine/ai/replay separation)
- [x] M2: AI bots (Random, Heuristic)
- [x] M3: Minimax + Alpha-Beta
- [x] M4: AI Coach + Replay Analyzer
- [x] M5: FastAPI service layer

---

## License

MIT
