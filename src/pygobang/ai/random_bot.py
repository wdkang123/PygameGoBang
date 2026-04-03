"""Random bot - selects a random valid move."""

import random
from typing import Tuple

from pygobang.ai.base import Bot
from pygobang.core.board import Board


class RandomBot(Bot):
    """Bot that selects a random valid move."""

    def next_move(self, board: Board, role: int) -> Tuple[int, int]:
        empty = board.get_all_empty()
        if not empty:
            raise ValueError("No empty positions available")
        return random.choice(empty)
