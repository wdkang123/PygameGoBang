"""Benchmark script for AI bots."""

import random
import time

from pygobang.ai.heuristic_bot import HeuristicBot
from pygobang.ai.minimax_bot import MiniMaxBot
from pygobang.ai.random_bot import RandomBot
from pygobang.core.board import Board
from pygobang.core.constants import BLACK, WHITE


def benchmark_bot(bot_class, name: str, board: Board, role: int, iterations: int = 5) -> float:
    """Benchmark a bot and return average decision time in ms."""
    bot = bot_class()
    times = []
    for _ in range(iterations):
        # Reset board to same state
        b = board.copy()
        start = time.time()
        x, y = bot.next_move(b, role)
        elapsed = (time.time() - start) * 1000
        times.append(elapsed)
    avg = sum(times) / len(times)
    print(f"{name}: avg={avg:.1f}ms min={min(times):.1f}ms max={max(times):.1f}ms")
    return avg


def random_board(moves: int = 10) -> Board:
    """Create a board with random moves."""
    b = Board(15)
    roles = [BLACK, WHITE]
    for i in range(moves):
        x, y = random.randint(0, 14), random.randint(0, 14)
        while not b.is_empty(x, y):
            x, y = random.randint(0, 14), random.randint(0, 14)
        b.set(x, y, roles[i % 2])
    return b


def main() -> None:
    print("=== AI Bot Benchmark ===")
    b = random_board(10)

    print("\nBoard with 10 random moves placed:")
    print(f"  Pieces: {b.count_pieces()}")
    print(f"  Candidates: {len(b.get_all_empty())}")

    print("\n--- RandomBot ---")
    benchmark_bot(RandomBot, "RandomBot", b, BLACK, 10)

    print("\n--- HeuristicBot ---")
    benchmark_bot(HeuristicBot, "HeuristicBot", b, BLACK, 10)

    print("\n--- MiniMaxBot depth=2 ---")
    benchmark_bot(lambda: MiniMaxBot(max_depth=2), "MiniMaxBot(d=2)", b, BLACK, 5)

    print("\n--- MiniMaxBot depth=3 ---")
    benchmark_bot(lambda: MiniMaxBot(max_depth=3), "MiniMaxBot(d=3)", b, BLACK, 3)

    print("\nBenchmark complete.")


if __name__ == "__main__":
    main()
