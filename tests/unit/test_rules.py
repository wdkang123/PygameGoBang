"""Unit tests for Rules."""

from pygobang.core.board import Board
from pygobang.core.constants import BLACK, WHITE
from pygobang.core.rules import Rules


class TestRules:
    def test_valid_move(self):
        b = Board(15)
        assert Rules.is_valid_move(b, 7, 7) is True
        b.set(7, 7, BLACK)
        assert Rules.is_valid_move(b, 7, 7) is False
        assert Rules.is_valid_move(b, 20, 20) is False

    def test_horizontal_win(self):
        b = Board(15)
        for x in range(5):
            b.set(x, 0, BLACK)
        assert Rules.check_winner(b, 4, 0, BLACK) == BLACK

    def test_vertical_win(self):
        b = Board(15)
        for y in range(5):
            b.set(0, y, WHITE)
        assert Rules.check_winner(b, 0, 4, WHITE) == WHITE

    def test_diagonal_win_positive(self):
        b = Board(15)
        for i in range(5):
            b.set(i, i, BLACK)
        assert Rules.check_winner(b, 4, 4, BLACK) == BLACK

    def test_diagonal_win_negative(self):
        b = Board(15)
        for i in range(5):
            b.set(i, 4 - i, WHITE)
        assert Rules.check_winner(b, 4, 0, WHITE) == WHITE

    def test_no_win(self):
        b = Board(15)
        b.set(0, 0, BLACK)
        b.set(1, 0, BLACK)
        b.set(2, 0, BLACK)
        assert Rules.check_winner(b, 0, 0, BLACK) is None

    def test_winning_line(self):
        b = Board(15)
        for x in range(5):
            b.set(x, 0, BLACK)
        line = Rules.get_winning_line(b, 2, 0, BLACK)
        assert len(line) == 5

    def test_board_full(self):
        b = Board(3)
        for y in range(3):
            for x in range(3):
                b.set(x, y, BLACK)
        assert Rules.is_board_full(b) is True
