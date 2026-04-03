"""Bot abstract base class."""

from abc import ABC, abstractmethod
from typing import Tuple


class Bot(ABC):
    """Abstract base class for all AI bots."""

    @abstractmethod
    def next_move(self, board, role: int) -> Tuple[int, int]:
        """
        Compute the next move for 'role' on 'board'.
        Returns (x, y) coordinates.
        Must return a valid empty position.
        """
        raise NotImplementedError
