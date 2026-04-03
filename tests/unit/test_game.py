"""Unit tests for Game."""

from pygobang.core.constants import BLACK, WHITE
from pygobang.core.game import Game


class TestGame:
    def test_init(self):
        g = Game()
        assert g.get_current_role() == BLACK
        assert g.get_move_count() == 0
        assert g.is_over() is False

    def test_make_move(self):
        g = Game()
        assert g.make_move(7, 7) is True
        assert g.get_move_count() == 1
        assert g.get_current_role() == WHITE

    def test_invalid_move(self):
        g = Game()
        g.make_move(7, 7)
        assert g.make_move(7, 7) is False  # occupied
        assert g.make_move(20, 20) is False  # out of bounds

    def test_undo(self):
        g = Game()
        g.make_move(7, 7)
        assert g.undo() is True
        assert g.get_move_count() == 0
        assert g.get_current_role() == BLACK

    def test_win_horizontal(self):
        # BLACK must play consecutive x=0..4 in row 0 while WHITE plays elsewhere
        g = Game()
        black_positions = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        white_positions = [(10, y) for y in range(1, 10, 2)]
        for bp, wp in zip(black_positions, white_positions, strict=True):
            g.make_move(*bp)
            g.make_move(*wp)
        assert g.get_winner() == BLACK

    def test_win_vertical(self):
        # BLACK plays consecutive y=0..4 in column 0 while WHITE plays elsewhere
        g = Game()
        black_positions = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
        white_positions = [(10, y) for y in range(1, 10, 2)]
        for bp, wp in zip(black_positions, white_positions, strict=True):
            g.make_move(*bp)
            g.make_move(*wp)
        assert g.get_winner() == BLACK

    def test_reset(self):
        g = Game()
        g.make_move(1, 1)
        g.reset()
        assert g.get_move_count() == 0
        assert g.get_winner() is None
