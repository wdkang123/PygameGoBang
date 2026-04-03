"""Game recorder - records moves during a game."""

import time
from dataclasses import asdict, dataclass
from typing import List, Optional

from pygobang.core.move import Move


@dataclass
class ReplayMeta:
    board_size: int = 15
    rule: str = "gomoku"
    started_at: str = ""
    ended_at: str = ""
    black_player: str = "human"
    white_player: str = "human"


@dataclass
class ReplayResult:
    winner: int
    reason: str


class Recorder:
    """Records moves during a game for later replay."""

    def __init__(self, board_size: int = 15) -> None:
        self.board_size = board_size
        self.moves: List[Move] = []
        self.meta = ReplayMeta()
        self.result: Optional[ReplayResult] = None
        self._started = False

    def start(self, black_player: str = "human", white_player: str = "human") -> None:
        """Start recording a new game."""
        self.moves.clear()
        self.meta = ReplayMeta(
            board_size=self.board_size,
            rule="gomoku",
            started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            black_player=black_player,
            white_player=white_player,
        )
        self.result = None
        self._started = True

    def record_move(self, move: Move) -> None:
        """Record a single move."""
        if not self._started:
            raise RuntimeError("Recorder not started")
        self.moves.append(move)

    def end(self, winner: Optional[int] = None, reason: str = "five_in_a_row") -> None:
        """End recording."""
        self.meta.ended_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        if winner:
            self.result = ReplayResult(winner=winner, reason=reason)
        self._started = False

    def get_moves(self) -> List[Move]:
        return self.moves.copy()

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "meta": asdict(self.meta),
            "moves": [{"step": m.step, "x": m.x, "y": m.y, "role": m.role} for m in self.moves],
            "result": asdict(self.result) if self.result else None,
        }
