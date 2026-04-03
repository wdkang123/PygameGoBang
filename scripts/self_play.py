"""Self-play script to generate test games."""

from pathlib import Path

from pygobang.ai.heuristic_bot import HeuristicBot
from pygobang.ai.random_bot import RandomBot
from pygobang.core.constants import BLACK
from pygobang.core.game import Game
from pygobang.replay.recorder import Recorder
from pygobang.replay.serializer import Serializer


def self_play(bot1, bot2, name1="bot1", name2="bot2", max_moves=225) -> Recorder:
    """Run a self-play game between two bots."""
    game = Game()
    recorder = Recorder()
    recorder.start(black_player=name1, white_player=name2)

    while not game.is_over() and game.get_move_count() < max_moves:
        role = game.get_current_role()
        if role == BLACK:
            x, y = bot1.next_move(game.board, role)
        else:
            x, y = bot2.next_move(game.board, role)

        game.make_move(x, y)
        move = game.moves[-1]
        recorder.record_move(move)

    winner = game.get_winner()
    recorder.end(winner=winner)
    return recorder


def main() -> None:
    print("=== Self-Play: HeuristicBot vs RandomBot ===")
    bot1 = HeuristicBot()
    bot2 = RandomBot()

    recorder = self_play(bot1, bot2, "heuristic", "random")

    out_dir = Path("examples/sample_replays")
    out_dir.mkdir(parents=True, exist_ok=True)

    path = out_dir / "self_play_heuristic_vs_random.json"
    Serializer.save(recorder, path)
    print(f"Saved to {path}")
    print(f"Winner: {'black' if recorder.result.winner == BLACK else 'white'}")
    print(f"Total moves: {len(recorder.get_moves())}")


if __name__ == "__main__":
    main()
