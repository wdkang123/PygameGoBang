"""Unit tests for Board."""

import pytest

from pygobang.core.board import Board
from pygobang.core.constants import BLACK, EMPTY, WHITE


class TestBoard:
    def test_init(self):
        b = Board(15)
        assert b.size == 15
        assert b.count_pieces() == 0

    def test_get_set(self):
        b = Board(15)
        b.set(7, 7, BLACK)
        assert b.get(7, 7) == BLACK
        assert b.is_empty(7, 7) is False

    def test_get_out_of_bounds(self):
        b = Board(15)
        with pytest.raises(IndexError):
            b.get(15, 7)

    def test_copy(self):
        b = Board(15)
        b.set(3, 3, WHITE)
        b2 = b.copy()
        b2.set(4, 4, BLACK)
        assert b.get(4, 4) == EMPTY

    def test_reset(self):
        b = Board(15)
        b.set(0, 0, BLACK)
        b.reset()
        assert b.is_empty(0, 0)

    def test_to_list(self):
        b = Board(15)
        b.set(0, 0, BLACK)
        lst = b.to_list()
        assert lst[0] == BLACK
        assert len(lst) == 225

    def test_from_list(self):
        data = [EMPTY] * 225
        data[0] = WHITE
        b = Board.from_list(data)
        assert b.get(0, 0) == WHITE
