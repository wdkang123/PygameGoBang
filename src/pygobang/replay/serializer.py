"""Replay serialization to/from JSON."""

import json
from pathlib import Path

from pygobang.core.move import Move
from pygobang.replay.recorder import Recorder, ReplayMeta


class Serializer:
    """Serialize and deserialize replay files."""

    @staticmethod
    def save(recorder: Recorder, path: Path) -> None:
        """Save a replay to a JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(recorder.to_dict(), f, indent=2, ensure_ascii=False)

    @staticmethod
    def load(path: Path) -> Recorder:
        """Load a replay from a JSON file."""
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        meta_data = data.get("meta", {})
        recorder = Recorder(board_size=meta_data.get("board_size", 15))
        recorder.meta = ReplayMeta(
            board_size=meta_data.get("board_size", 15),
            rule=meta_data.get("rule", "gomoku"),
            started_at=meta_data.get("started_at", ""),
            ended_at=meta_data.get("ended_at", ""),
            black_player=meta_data.get("black_player", "human"),
            white_player=meta_data.get("white_player", "human"),
        )
        recorder.start(
            black_player=meta_data.get("black_player", "human"),
            white_player=meta_data.get("white_player", "human"),
        )

        for m in data.get("moves", []):
            move = Move(
                x=m["x"],
                y=m["y"],
                role=m["role"],
                step=m["step"],
            )
            recorder.record_move(move)

        result = data.get("result")
        if result:
            recorder.end(
                winner=result["winner"],
                reason=result.get("reason", "five_in_a_row"),
            )
        else:
            recorder.end()

        return recorder
