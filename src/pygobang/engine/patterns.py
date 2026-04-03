"""Pattern definitions for Gomoku evaluation."""

from enum import IntEnum


class Pattern(IntEnum):
    """Gomoku pattern types with associated scores."""

    FIVE = 1_000_000
    LIVE_FOUR = 100_000
    RUSH_FOUR = 10_000
    LIVE_THREE = 5_000
    SLEEP_THREE = 1_000
    LIVE_TWO = 200
    SLEEP_TWO = 50
    LIVE_ONE = 10


class Patterns:
    """Pattern detection utilities."""

    @staticmethod
    def count_pattern_in_line(board, x: int, y: int, dx: int, dy: int, role: int) -> int:
        """Count consecutive pieces of 'role' starting from (x, y) in direction (dx, dy)."""
        count = 0
        while 0 <= x < board.size and 0 <= y < board.size and board.get(x, y) == role:
            count += 1
            x += dx
            y += dy
        return count
