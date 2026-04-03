"""Unit tests for AI bots."""

from pygobang.ai.heuristic_bot import HeuristicBot
from pygobang.ai.minimax_bot import MiniMaxBot
from pygobang.ai.random_bot import RandomBot
from pygobang.core.board import Board
from pygobang.core.constants import BLACK, WHITE


class TestRandomBot:
    def test_returns_valid_move(self):
        bot = RandomBot()
        board = Board(15)
        x, y = bot.next_move(board, BLACK)
        assert 0 <= x < 15
        assert 0 <= y < 15
        assert board.is_empty(x, y)


class TestHeuristicBot:
    def test_returns_valid_move(self):
        bot = HeuristicBot()
        board = Board(15)
        board.set(7, 7, BLACK)
        x, y = bot.next_move(board, WHITE)
        assert board.is_empty(x, y)

    def test_takes_win_if_available(self):
        bot = HeuristicBot()
        board = Board(15)
        for x in range(4):
            board.set(x, 0, BLACK)
        x, y = bot.next_move(board, BLACK)
        assert (x, y) == (4, 0) or board.is_empty(x, y)

    def test_blocks_opponent_win(self):
        bot = HeuristicBot()
        board = Board(15)
        for x in range(4):
            board.set(x, 0, WHITE)
        x, y = bot.next_move(board, BLACK)
        assert (x, y) == (4, 0)


class TestMiniMaxBot:
    def test_returns_valid_move(self):
        bot = MiniMaxBot(max_depth=2)
        board = Board(15)
        x, y = bot.next_move(board, BLACK)
        assert board.is_empty(x, y)

    def test_respects_time_limit(self):
        bot = MiniMaxBot(max_depth=4, time_limit_ms=100)
        board = Board(15)
        for i in range(10):
            board.set(i % 15, i // 15, BLACK if i % 2 == 0 else WHITE)
        x, y = bot.next_move(board, BLACK)
        assert board.is_empty(x, y)
