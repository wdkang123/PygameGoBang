"""Move dataclass."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Move:
    """Represents a single move in the game."""

    x: int
    y: int
    role: int
    step: int
    timestamp_ms: Optional[int] = None

    def __post_init__(self) -> None:
        if self.role not in (1, 2):
            raise ValueError(f"Invalid role: {self.role}")
        if not (0 <= self.x < 15 and 0 <= self.y < 15):
            raise ValueError(f"Invalid coordinates: ({self.x}, {self.y})")
