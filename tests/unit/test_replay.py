"""Unit tests for Replay system."""

import tempfile
from pathlib import Path

from pygobang.core.constants import BLACK
from pygobang.core.game import Game
from pygobang.replay.recorder import Recorder
from pygobang.replay.serializer import Serializer


class TestRecorder:
    def test_start_end(self):
        r = Recorder()
        r.start(black_player="human", white_player="ai")
        r.record_move(
            __import__("pygobang.core.move", fromlist=["Move"]).Move(x=7, y=7, role=BLACK, step=1)
        )
        r.end(winner=BLACK)
        assert r.result.winner == BLACK


class TestSerializer:
    def test_save_load(self):
        # Create a game where BLACK wins horizontally
        game = Game()
        black_positions = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        white_positions = [(10, y) for y in range(1, 10, 2)]
        for bp, wp in zip(black_positions, white_positions, strict=True):
            game.make_move(*bp)
            game.make_move(*wp)

        recorder = Recorder()
        recorder.start(black_player="human", white_player="ai")
        for m in game.moves:
            recorder.record_move(m)
        recorder.end(winner=game.get_winner())

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            tmp = Path(f.name)

        try:
            Serializer.save(recorder, tmp)
            loaded = Serializer.load(tmp)
            assert loaded.result.winner == BLACK
            assert len(loaded.get_moves()) == 9  # game ends after BLACK's 5th move, no response
        finally:
            tmp.unlink()
