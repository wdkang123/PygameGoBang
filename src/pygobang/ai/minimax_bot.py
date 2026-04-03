"""Minimax bot with alpha-beta pruning."""

import time
from typing import Optional, Tuple

from pygobang.ai.base import Bot
from pygobang.core.board import Board
from pygobang.core.constants import EMPTY
from pygobang.engine.candidate_generator import CandidateGenerator
from pygobang.engine.evaluator import Evaluator


class MiniMaxBot(Bot):
    """Minimax search with alpha-beta pruning."""

    def __init__(
        self,
        max_depth: int = 4,
        max_candidates: int = 12,
        time_limit_ms: Optional[int] = None,
    ) -> None:
        self.max_depth = max_depth
        self.candidate_gen = CandidateGenerator(max_candidates)
        self.time_limit_ms = time_limit_ms

    def next_move(self, board: Board, role: int) -> Tuple[int, int]:
        start = time.time()

        # Check for immediate win/block first
        candidates = self.candidate_gen.generate(board, role)
        for x, y in candidates:
            board.set(x, y, role)
            from pygobang.core.rules import Rules

            if Rules.check_winner(board, x, y, role):
                board.set(x, y, EMPTY)
                return (x, y)
            board.set(x, y, EMPTY)

        opponent = 2 if role == 1 else 1
        for x, y in candidates:
            board.set(x, y, opponent)
            from pygobang.core.rules import Rules

            if Rules.check_winner(board, x, y, opponent):
                board.set(x, y, EMPTY)
                return (x, y)
            board.set(x, y, EMPTY)

        best_score = -float("inf")
        best_move = candidates[0] if candidates else (7, 7)
        alpha = -float("inf")
        beta = float("inf")

        for x, y in candidates:
            if self.time_limit_ms and (time.time() - start) * 1000 > self.time_limit_ms:
                break

            board.set(x, y, role)
            score = self._minimax(board, self.max_depth - 1, alpha, beta, False, role, opponent)
            board.set(x, y, EMPTY)

            if score > best_score:
                best_score = score
                best_move = (x, y)
            alpha = max(alpha, score)

        return best_move

    def _minimax(
        self,
        board: Board,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
        role: int,
        opponent: int,
    ) -> float:
        """Minimax with alpha-beta pruning."""
        if depth == 0:
            return Evaluator.evaluate(board, role)

        candidates = self.candidate_gen.generate(board, opponent if not maximizing else role)

        if not candidates:
            return Evaluator.evaluate(board, role)

        if maximizing:
            best = -float("inf")
            for x, y in candidates:
                board.set(x, y, role)
                score = self._minimax(board, depth - 1, alpha, beta, False, role, opponent)
                board.set(x, y, EMPTY)
                best = max(best, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best
        else:
            best = float("inf")
            for x, y in candidates:
                board.set(x, y, opponent)
                score = self._minimax(board, depth - 1, alpha, beta, True, role, opponent)
                board.set(x, y, EMPTY)
                best = min(best, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best
