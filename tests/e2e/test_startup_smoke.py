"""E2E smoke test."""


def test_import_core():
    from pygobang.core import Game

    g = Game()
    assert g.get_current_role() == 1


def test_import_ai():
    from pygobang.ai import HeuristicBot, MiniMaxBot, RandomBot
    from pygobang.core.board import Board

    bots = [RandomBot(), HeuristicBot(), MiniMaxBot(max_depth=2)]
    for bot in bots:
        b = Board()
        x, y = bot.next_move(b, 1)
        assert 0 <= x < 15


def test_import_replay():
    from pygobang.replay import Recorder

    r = Recorder()
    r.start()


def test_full_game_simulation():
    from pygobang.ai.heuristic_bot import HeuristicBot
    from pygobang.core.game import Game

    game = Game()
    ai = HeuristicBot()

    # Play a limited number of moves to avoid timeout
    for _ in range(50):
        if game.is_over():
            break
        role = game.get_current_role()
        x, y = ai.next_move(game.board, role) if role != 1 else (7, 7)
        game.make_move(x, y)

    assert game.get_move_count() > 0
