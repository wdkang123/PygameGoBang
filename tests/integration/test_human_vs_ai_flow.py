"""Integration test: human vs AI flow."""

from pygobang.ai.heuristic_bot import HeuristicBot
from pygobang.core.constants import BLACK
from pygobang.core.game import Game


def test_full_game_vs_ai():
    """Simulate a complete game between human and AI."""
    game = Game()
    ai = HeuristicBot()

    moves_made = 0
    max_moves = 225
    black_moves = [(7, 7), (7, 8), (6, 7), (8, 7), (7, 6), (7, 9), (6, 8)]
    black_idx = 0

    while not game.is_over() and moves_made < max_moves:
        role = game.get_current_role()
        if role == BLACK:
            x, y = black_moves[black_idx]
            black_idx = min(black_idx + 1, len(black_moves) - 1)
        else:
            x, y = ai.next_move(game.board, role)

        result = game.make_move(x, y)
        if role == BLACK:
            assert result is True
        moves_made += 1

    assert game.is_over()
    assert game.get_winner() is not None


def test_ai_never_makes_invalid_move():
    """AI always returns valid empty position."""
    ai = HeuristicBot()
    for _ in range(20):
        game = Game()
        for _ in range(30):
            if game.is_over():
                break
            x, y = ai.next_move(game.board, game.get_current_role())
            assert game.board.is_empty(x, y)
            game.make_move(x, y)
