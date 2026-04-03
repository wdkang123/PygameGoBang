"""Game rules: win detection and move validation."""

from typing import List, Optional, Tuple

from pygobang.core.board import Board
from pygobang.core.constants import EMPTY


class Rules:
    """Gomoku rules implementation."""

    DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]

    @staticmethod
    def is_valid_move(board: Board, x: int, y: int) -> bool:
        """Check if a move is valid (within bounds and on empty spot)."""
        if not (0 <= x < board.size and 0 <= y < board.size):
            return False
        return board.is_empty(x, y)

    @staticmethod
    def check_winner(board: Board, last_x: int, last_y: int, last_role: int) -> Optional[int]:
        """
        Check if last move at (last_x, last_y) by 'last_role' creates a five-in-a-row.
        Returns winner's role (1 or 2) if someone won, None otherwise.
        """
        for dx, dy in Rules.DIRECTIONS:
            count = 1
            # Count forward
            x, y = last_x + dx, last_y + dy
            while 0 <= x < board.size and 0 <= y < board.size and board.get(x, y) == last_role:
                count += 1
                x += dx
                y += dy
            # Count backward
            x, y = last_x - dx, last_y - dy
            while 0 <= x < board.size and 0 <= y < board.size and board.get(x, y) == last_role:
                count += 1
                x -= dx
                y -= dy
            if count >= 5:
                return last_role
        return None

    @staticmethod
    def get_winning_line(
        board: Board, last_x: int, last_y: int, last_role: int
    ) -> List[Tuple[int, int]]:
        """Return the 5-tuple positions that constitute the winning line."""
        for dx, dy in Rules.DIRECTIONS:
            line = [(last_x, last_y)]
            # Collect forward
            x, y = last_x + dx, last_y + dy
            while 0 <= x < board.size and 0 <= y < board.size and board.get(x, y) == last_role:
                line.append((x, y))
                x += dx
                y += dy
            # Collect backward
            x, y = last_x - dx, last_y - dy
            while 0 <= x < board.size and 0 <= y < board.size and board.get(x, y) == last_role:
                line.insert(0, (x, y))
                x -= dx
                y -= dy
            if len(line) >= 5:
                return line[:5]
        return []

    @staticmethod
    def is_board_full(board: Board) -> bool:
        """Check if board has no empty spots."""
        return EMPTY not in board.to_list()
