"""Board representation."""

from typing import List, Tuple

from pygobang.core.constants import EMPTY


class Board:
    """15x15 Gomoku board using a flat list for efficiency."""

    def __init__(self, size: int = 15) -> None:
        self.size = size
        self._grid: List[int] = [EMPTY] * (size * size)

    def get(self, x: int, y: int) -> int:
        """Get piece at (x, y). Returns EMPTY, BLACK, or WHITE."""
        if not (0 <= x < self.size and 0 <= y < self.size):
            raise IndexError(f"Coordinates ({x}, {y}) out of bounds")
        return self._grid[y * self.size + x]

    def set(self, x: int, y: int, value: int) -> None:
        """Set piece at (x, y)."""
        if not (0 <= x < self.size and 0 <= y < self.size):
            raise IndexError(f"Coordinates ({x}, {y}) out of bounds")
        self._grid[y * self.size + x] = value

    def is_empty(self, x: int, y: int) -> bool:
        """Check if position is empty."""
        return self.get(x, y) == EMPTY

    def get_all_empty(self) -> List[Tuple[int, int]]:
        """Return all empty positions."""
        result = []
        for i, v in enumerate(self._grid):
            if v == EMPTY:
                x = i % self.size
                y = i // self.size
                result.append((x, y))
        return result

    def count_pieces(self) -> int:
        """Count non-empty pieces."""
        return sum(1 for v in self._grid if v != EMPTY)

    def copy(self) -> "Board":
        """Return a deep copy of the board."""
        new = Board(self.size)
        new._grid = self._grid.copy()
        return new

    def reset(self) -> None:
        """Clear the board."""
        self._grid = [EMPTY] * (self.size * self.size)

    def to_list(self) -> List[int]:
        """Return flat list representation."""
        return self._grid.copy()

    @classmethod
    def from_list(cls, data: List[int], size: int = 15) -> "Board":
        """Reconstruct board from flat list."""
        board = cls(size)
        board._grid = data.copy()
        return board
