"""Board evaluation functions."""

from typing import Tuple

from pygobang.core.board import Board
from pygobang.core.constants import BLACK, EMPTY, WHITE
from pygobang.engine.patterns import Pattern


class Evaluator:
    """Evaluates board positions for AI decision making."""

    DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]

    @staticmethod
    def evaluate(board: Board, role: int) -> int:
        """
        Evaluate board from perspective of 'role'.
        Returns a score (higher = better for role).
        """
        opponent = WHITE if role == BLACK else BLACK
        return Evaluator._evaluate_for(board, role) - Evaluator._evaluate_for(board, opponent)

    @staticmethod
    def _evaluate_for(board: Board, role: int) -> int:
        """Calculate score for a specific role."""
        score = 0
        checked = set()

        for y in range(board.size):
            for x in range(board.size):
                if board.get(x, y) == role:
                    for dx, dy in Evaluator.DIRECTIONS:
                        key = (x, y, dx, dy)
                        if key in checked:
                            continue
                        checked.add(key)

                        count, open_ends = Evaluator._analyze_line(board, x, y, dx, dy, role)
                        score += Evaluator._score_from_count(count, open_ends)

        return score

    @staticmethod
    def _analyze_line(board: Board, x: int, y: int, dx: int, dy: int, role: int) -> Tuple[int, int]:
        """Analyze a line of pieces: returns (count, open_ends)."""
        count = 0
        open_ends = 0

        # Forward
        cx, cy = x, y
        while 0 <= cx < board.size and 0 <= cy < board.size and board.get(cx, cy) == role:
            count += 1
            cx += dx
            cy += dy

        if 0 <= cx < board.size and 0 <= cy < board.size and board.get(cx, cy) == EMPTY:
            open_ends += 1

        # Backward
        bx, by = x - dx, y - dy
        if 0 <= bx < board.size and 0 <= by < board.size and board.get(bx, by) == EMPTY:
            open_ends += 1

        return count, open_ends

    @staticmethod
    def _score_from_count(count: int, open_ends: int) -> int:
        """Map count+open_ends to a pattern score."""
        if count >= 5:
            return Pattern.FIVE
        if count == 4:
            if open_ends == 2:
                return Pattern.LIVE_FOUR
            if open_ends == 1:
                return Pattern.RUSH_FOUR
        if count == 3:
            if open_ends == 2:
                return Pattern.LIVE_THREE
            if open_ends == 1:
                return Pattern.SLEEP_THREE
        if count == 2:
            if open_ends == 2:
                return Pattern.LIVE_TWO
            if open_ends == 1:
                return Pattern.SLEEP_TWO
        if count == 1 and open_ends == 2:
            return Pattern.LIVE_ONE
        return 0
