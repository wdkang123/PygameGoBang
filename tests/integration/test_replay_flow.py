"""Integration test: replay serialization and analysis."""

import tempfile
from pathlib import Path

from pygobang.ai.heuristic_bot import HeuristicBot
from pygobang.core.constants import BLACK
from pygobang.core.game import Game
from pygobang.replay.analyzer import ReplayAnalyzer
from pygobang.replay.recorder import Recorder
from pygobang.replay.serializer import Serializer


def test_full_replay_flow():
    """Test complete replay: record -> save -> load -> analyze."""
    game = Game()
    recorder = Recorder()
    recorder.start(black_player="human", white_player="heuristic")

    ai = HeuristicBot()
    black_moves = [(7, 7), (7, 8), (6, 7), (8, 7), (7, 6), (6, 8), (8, 6)]
    black_idx = 0

    while not game.is_over() and game.get_move_count() < 20:
        role = game.get_current_role()
        if role == BLACK:
            x, y = black_moves[black_idx]
            black_idx = min(black_idx + 1, len(black_moves) - 1)
        else:
            x, y = ai.next_move(game.board, role)

        if game.make_move(x, y):
            recorder.record_move(game.moves[-1])

    recorder.end(winner=game.get_winner())

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "test_replay.json"
        Serializer.save(recorder, path)
        assert path.exists()

        loaded = Serializer.load(path)
        assert len(loaded.get_moves()) == len(recorder.get_moves())

        analyzer = ReplayAnalyzer()
        result = analyzer.analyze(loaded)
        assert result.total_moves == len(loaded.get_moves())
        assert result.winner in (1, 2)
