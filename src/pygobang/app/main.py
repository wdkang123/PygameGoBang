"""Main application entry point."""

import argparse

from pygobang.ai.heuristic_bot import HeuristicBot
from pygobang.ai.minimax_bot import MiniMaxBot
from pygobang.ai.random_bot import RandomBot
from pygobang.ui.pygame_app import PygameApp


def main() -> None:
    parser = argparse.ArgumentParser(description="PygameGoBang - AI Gomoku Platform")
    parser.add_argument(
        "--opponent",
        choices=["random", "heuristic", "minimax"],
        default=None,
        help="AI opponent type (default: human vs human)",
    )
    parser.add_argument("--depth", type=int, default=4, help="Minimax depth")
    args = parser.parse_args()

    opponent = None
    if args.opponent == "random":
        opponent = RandomBot()
    elif args.opponent == "heuristic":
        opponent = HeuristicBot()
    elif args.opponent == "minimax":
        opponent = MiniMaxBot(max_depth=args.depth)

    app = PygameApp(opponent_bot=opponent)
    app.run()


if __name__ == "__main__":
    main()
