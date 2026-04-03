"""Candidate move generation for AI search."""

from typing import List, Tuple

from pygobang.core.board import Board
from pygobang.core.constants import BLACK, WHITE
from pygobang.engine.state import GameState


class CandidateGenerator:
    """Generates and ranks candidate moves for AI consideration."""

    def __init__(self, max_candidates: int = 16) -> None:
        self.max_candidates = max_candidates

    def generate(self, board: Board, current_role: int) -> List[Tuple[int, int]]:
        """Generate ranked candidate moves ordered by priority."""
        state = GameState(board, current_role)
        candidates = []

        for x, y in state.get_neighbor_positions(radius=2):
            if board.is_empty(x, y):
                score = self._quick_score(board, x, y, current_role)
                candidates.append((x, y, score))

        candidates.sort(key=lambda c: c[2], reverse=True)
        return [(x, y) for x, y, _ in candidates[: self.max_candidates]]

    @staticmethod
    def _quick_score(board: Board, x: int, y: int, role: int) -> int:
        """Quick heuristic score for a candidate move."""
        opponent = WHITE if role == BLACK else BLACK
        score = 0
        for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
            own_count = 0
            opp_count = 0
            for d in range(1, 5):
                nx1, ny1 = x + dx * d, y + dy * d
                nx2, ny2 = x - dx * d, y - dy * d
                if 0 <= nx1 < board.size and 0 <= ny1 < board.size:
                    if board.get(nx1, ny1) == role:
                        own_count += 1
                    if board.get(nx1, ny1) == opponent:
                        opp_count += 1
                if 0 <= nx2 < board.size and 0 <= ny2 < board.size:
                    if board.get(nx2, ny2) == role:
                        own_count += 1
                    if board.get(nx2, ny2) == opponent:
                        opp_count += 1
            score += own_count * 10 + opp_count * 8
        return score
