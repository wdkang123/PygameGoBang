"""Unit tests for Evaluator."""

from pygobang.core.board import Board
from pygobang.core.constants import BLACK
from pygobang.engine.evaluator import Evaluator


class TestEvaluator:
    def test_empty_board(self):
        b = Board(15)
        score = Evaluator.evaluate(b, BLACK)
        assert score == 0

    def test_single_piece(self):
        b = Board(15)
        b.set(7, 7, BLACK)
        # Some score but not zero
        score = Evaluator.evaluate(b, BLACK)
        assert score > 0

    def test_five_in_row(self):
        b = Board(15)
        for x in range(5):
            b.set(x, 0, BLACK)
        score = Evaluator.evaluate(b, BLACK)
        assert score >= 1_000_000
