"""Replay analyzer for post-game analysis."""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from pygobang.core.board import Board
from pygobang.engine.evaluator import Evaluator
from pygobang.replay.recorder import Recorder


@dataclass
class MoveAnalysis:
    step: int
    x: int
    y: int
    role: int
    score_before: int
    score_after: int
    is_critical: bool = False
    is_blunder: bool = False
    best_alternative: Optional[Tuple[int, int]] = None


@dataclass
class ReplayAnalysis:
    winner: int
    total_moves: int
    critical_moves: List[int]
    blunders: List[int]
    best_alternatives: Dict[int, Tuple[int, int]]
    style_analysis: Dict[str, str]
    training_suggestions: List[str]

    def to_dict(self) -> dict:
        return {
            "winner": "black" if self.winner == 1 else "white",
            "total_moves": self.total_moves,
            "critical_moves": self.critical_moves,
            "blunders": self.blunders,
            "best_alternatives": {str(k): list(v) for k, v in self.best_alternatives.items()},
            "style_analysis": self.style_analysis,
            "training_suggestions": self.training_suggestions,
        }


class ReplayAnalyzer:
    """Analyzes a recorded game and generates structured feedback."""

    def analyze(self, recorder: Recorder) -> ReplayAnalysis:
        """Perform full game analysis."""
        moves = recorder.get_moves()
        if not moves:
            raise ValueError("No moves to analyze")

        board = Board(recorder.board_size)
        move_analyses: List[MoveAnalysis] = []
        blunders: List[int] = []
        critical_moves: List[int] = []
        best_alternatives: Dict[int, Tuple[int, int]] = {}

        player_role = moves[0].role

        for i, move in enumerate(moves):
            score_before = Evaluator.evaluate(board, player_role)

            board.set(move.x, move.y, move.role)
            score_after = Evaluator.evaluate(board, player_role)

            # Simple blunder detection: large eval drop
            eval_drop = score_before - score_after
            is_blunder = eval_drop > 3000 and i > 3

            if is_blunder:
                blunders.append(move.step)

            # Critical move: when eval changes significantly
            if abs(eval_drop) > 2000 or abs(score_after) > 5000:
                critical_moves.append(move.step)

            move_analyses.append(
                MoveAnalysis(
                    step=move.step,
                    x=move.x,
                    y=move.y,
                    role=move.role,
                    score_before=score_before,
                    score_after=score_after,
                    is_blunder=is_blunder,
                )
            )

        winner = recorder.result.winner if recorder.result else moves[-1].role

        # Generate training suggestions
        suggestions = []
        if len(blunders) > 0:
            suggestions.append(f"共识别 {len(blunders)} 步失误，建议加强棋形识别训练")
        if critical_moves:
            suggestions.append("关键节点处理需更谨慎，建议分析此类局面的优先选项")

        black_style = (
            "偏进攻"
            if sum(1 for m in move_analyses if m.role == 1 and m.score_after > 0) > len(moves) // 4
            else "攻守平衡"
        )
        white_style = (
            "偏防守"
            if sum(1 for m in move_analyses if m.role == 2 and m.score_after < 0) > len(moves) // 4
            else "攻守平衡"
        )

        return ReplayAnalysis(
            winner=winner,
            total_moves=len(moves),
            critical_moves=critical_moves,
            blunders=blunders,
            best_alternatives=best_alternatives,
            style_analysis={"black": black_style, "white": white_style},
            training_suggestions=suggestions,
        )
