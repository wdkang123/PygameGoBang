"""Heuristic bot - uses pattern evaluation."""

from typing import Tuple

from pygobang.ai.base import Bot
from pygobang.core.board import Board
from pygobang.core.rules import Rules
from pygobang.engine.candidate_generator import CandidateGenerator
from pygobang.engine.evaluator import Evaluator


class HeuristicBot(Bot):
    """Bot that uses heuristic evaluation to pick the best move."""

    def __init__(self, max_candidates: int = 12) -> None:
        self.candidate_gen = CandidateGenerator(max_candidates)

    def next_move(self, board: Board, role: int) -> Tuple[int, int]:
        candidates = self.candidate_gen.generate(board, role)

        if not candidates:
            # Fallback: find any empty spot
            all_empty = board.get_all_empty()
            if not all_empty:
                raise ValueError("Board is full")
            return all_empty[0]

        # Also check for immediate win or block
        for x, y in candidates:
            if Rules.check_winner(board, x, y, role):
                return (x, y)

        # Block opponent's winning move
        opponent = 2 if role == 1 else 1
        for x, y in candidates:
            if Rules.check_winner(board, x, y, opponent):
                return (x, y)

        # Pick best by evaluation
        best_score = -float("inf")
        best_move = candidates[0]

        for x, y in candidates:
            board.set(x, y, role)
            score = Evaluator.evaluate(board, role)
            board.set(x, y, 0)  # undo
            if score > best_score:
                best_score = score
                best_move = (x, y)

        return best_move
