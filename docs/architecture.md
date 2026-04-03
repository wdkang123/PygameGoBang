# Architecture

## Overview

PygameGoBang is organized as a layered Python package.

```
src/pygobang/
├── core/      # Pure game logic (no UI, no network)
├── engine/    # Shared AI evaluation infrastructure
├── ai/        # Bot implementations + advisor
├── replay/    # Game recording and analysis
├── ui/        # Pygame presentation layer
├── infra/     # Logging, config
└── app/       # Application entry point
```

## Core (`core/`)

- `board.py` - Board representation (flat list, 15×15)
- `rules.py` - Win detection, move validation
- `game.py` - Full game state machine
- `move.py` - Immutable Move dataclass
- `constants.py` - EMPTY/BLACK/WHITE, board size

**Dependencies:** None (pure Python)

## Engine (`engine/`)

- `evaluator.py` - Pattern-based board evaluation
- `candidate_generator.py` - Neighbor-based candidate pruning
- `patterns.py` - Gomoku pattern scores
- `state.py` - Immutable game state wrapper

**Used by:** All AI bots

## AI (`ai/`)

- `base.py` - `Bot` ABC
- `random_bot.py` - Random valid move
- `heuristic_bot.py` - Pattern evaluation greedy
- `minimax_bot.py` - Minimax + Alpha-Beta
- `advisor.py` - Real-time game coach

## Replay (`replay/`)

- `recorder.py` - In-game move recording
- `serializer.py` - JSON save/load
- `parser.py` - Board reconstruction
- `analyzer.py` - Post-game analysis

## UI (`ui/`)

- `pygame_app.py` - Main Pygame loop

## Data Flow

```
UI → Game.make_move() → Board.set() + Rules.check_winner()
                         ↓
                    Recorder.record_move()
                         ↓
                    (optional) AI Advisor.analyze()
                         ↓
                    (optional) AI Bot.next_move()
```

## Running

```bash
# Human vs Human
python -m pygobang.app.main

# Human vs AI
python -m pygobang.app.main --opponent heuristic

# Human vs Minimax AI
python -m pygobang.app.main --opponent minimax --depth 4

# Run tests
make test

# Benchmark AI
make benchmark
```
