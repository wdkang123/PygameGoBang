"""Game state wrapper for engine evaluation."""

from typing import List, Optional, Tuple

from pygobang.core.board import Board
from pygobang.core.constants import BLACK, EMPTY, WHITE


class GameState:
    """Immutable view of game state for AI evaluation."""

    def __init__(
        self, board: Board, current_role: int, last_move: Optional[Tuple[int, int]] = None
    ) -> None:
        self.board = board
        self.current_role = current_role
        self.last_move = last_move

    def get_opponent(self, role: int) -> int:
        return WHITE if role == BLACK else BLACK

    def get_neighbor_positions(self, radius: int = 2) -> List[Tuple[int, int]]:
        """Get all positions within radius of any placed piece."""
        neighbors = set()
        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.get(x, y) != EMPTY:
                    for dy in range(-radius, radius + 1):
                        for dx in range(-radius, radius + 1):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.board.size and 0 <= ny < self.board.size:
                                if self.board.is_empty(nx, ny):
                                    neighbors.add((nx, ny))
        return list(neighbors)
