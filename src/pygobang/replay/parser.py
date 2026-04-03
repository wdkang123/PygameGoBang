"""Parser for loading and replaying saved games."""

from typing import Iterator, Tuple

from pygobang.core.board import Board
from pygobang.core.move import Move
from pygobang.replay.recorder import Recorder


class Parser:
    """Parse and reconstruct games from recordings."""

    @staticmethod
    def replay_moves(recorder: Recorder) -> Iterator[Tuple[Board, Move]]:
        """Yield (board_state, move) pairs for replaying a game."""
        board = Board(recorder.board_size)
        for move in recorder.get_moves():
            board.set(move.x, move.y, move.role)
            yield board.copy(), move

    @staticmethod
    def get_final_board(recorder: Recorder) -> Board:
        """Return the final board state after all moves."""
        board = Board(recorder.board_size)
        for move in recorder.get_moves():
            board.set(move.x, move.y, move.role)
        return board
