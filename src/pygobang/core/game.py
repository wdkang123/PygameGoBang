"""Game state management."""

import time
from typing import List, Optional

from pygobang.core.board import Board
from pygobang.core.constants import BLACK, EMPTY, WHITE
from pygobang.core.move import Move
from pygobang.core.rules import Rules


class Game:
    """Manages the full game state including move history."""

    def __init__(self, size: int = 15) -> None:
        self.board = Board(size)
        self.size = size
        self.moves: List[Move] = []
        self.current_role = BLACK
        self.winner: Optional[int] = None
        self.winning_line: List[tuple] = []
        self._start_time_ms = int(time.time() * 1000)

    def reset(self) -> None:
        """Reset the game to initial state."""
        self.board.reset()
        self.moves.clear()
        self.current_role = BLACK
        self.winner = None
        self.winning_line = []
        self._start_time_ms = int(time.time() * 1000)

    def make_move(self, x: int, y: int) -> bool:
        """
        Attempt to place a piece at (x, y) for current player.
        Returns True if move was successful, False otherwise.
        """
        if self.is_over():
            return False

        if not Rules.is_valid_move(self.board, x, y):
            return False

        step = len(self.moves) + 1
        timestamp = int(time.time() * 1000) - self._start_time_ms
        move = Move(x=x, y=y, role=self.current_role, step=step, timestamp_ms=timestamp)
        self.moves.append(move)
        self.board.set(x, y, self.current_role)

        winner = Rules.check_winner(self.board, x, y, self.current_role)
        if winner:
            self.winner = winner
            self.winning_line = Rules.get_winning_line(self.board, x, y, self.current_role)

        self.current_role = WHITE if self.current_role == BLACK else BLACK
        return True

    def undo(self) -> bool:
        """Undo the last move. Returns True if undo successful."""
        if not self.moves:
            return False
        move = self.moves.pop()
        self.board.set(move.x, move.y, EMPTY)
        self.winner = None
        self.winning_line = []
        self.current_role = move.role
        return True

    def is_over(self) -> bool:
        """Check if game is over (win or draw)."""
        if self.winner is not None:
            return True
        return Rules.is_board_full(self.board)

    def get_winner(self) -> Optional[int]:
        return self.winner

    def is_draw(self) -> bool:
        return self.is_over() and self.winner is None

    def get_move_count(self) -> int:
        return len(self.moves)

    def get_current_role(self) -> int:
        return self.current_role
