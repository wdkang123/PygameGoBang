"""AI Advisor - provides real-time game analysis and coaching."""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from pygobang.core.board import Board
from pygobang.core.constants import BLACK, WHITE
from pygobang.core.rules import Rules
from pygobang.engine.candidate_generator import CandidateGenerator
from pygobang.engine.evaluator import Evaluator


@dataclass
class AdvisorOutput:
    best_move: Tuple[int, int]
    top_moves: List[Tuple[int, int]]
    player_move_score: int
    position_eval: int
    phase: str
    advice: Dict[str, str]

    def to_dict(self) -> dict:
        return {
            "best_move": list(self.best_move),
            "top_moves": [list(m) for m in self.top_moves],
            "player_move_score": self.player_move_score,
            "position_eval": self.position_eval,
            "phase": self.phase,
            "advice": self.advice,
        }


class Advisor:
    """Real-time game advisor and coach."""

    def __init__(self) -> None:
        self.candidate_gen = CandidateGenerator(max_candidates=16)

    def analyze(
        self, board: Board, current_role: int, last_move: Optional[Tuple[int, int]] = None
    ) -> AdvisorOutput:
        """Analyze current position and return structured advice."""
        opponent = WHITE if current_role == BLACK else BLACK

        # Current evaluation
        position_eval = Evaluator.evaluate(board, current_role)

        # Phase detection
        piece_count = board.count_pieces()
        if piece_count < 10:
            phase = "opening"
        elif piece_count < 50:
            phase = "midgame"
        else:
            phase = "endgame"

        # Generate candidate moves
        candidates = self.candidate_gen.generate(board, current_role)

        # Top 3 moves
        top_moves = candidates[:3]

        # Best move
        best_move = top_moves[0] if top_moves else (7, 7)

        # Score last move if provided
        player_move_score = 0
        if last_move:
            eval_before = Evaluator.evaluate(board, current_role)
            # Simulate removing last move for comparison
            board.set(last_move[0], last_move[1], 0)
            eval_after = Evaluator.evaluate(board, current_role)
            board.set(last_move[0], last_move[1], current_role)
            player_move_score = int(eval_before - eval_after)

        # Generate advice
        advice = self._generate_advice(
            board, current_role, opponent, position_eval, phase, candidates
        )

        return AdvisorOutput(
            best_move=best_move,
            top_moves=top_moves,
            player_move_score=player_move_score,
            position_eval=position_eval,
            phase=phase,
            advice=advice,
        )

    def _generate_advice(
        self,
        board: Board,
        role: int,
        opponent: int,
        position_eval: int,
        phase: str,
        candidates: List[Tuple[int, int]],
    ) -> Dict[str, str]:
        """Generate natural language advice."""
        style = "offense" if position_eval > 0 else "defense"

        advice = {
            "style": style,
            "summary": "局势均势，建议谨慎落子",
            "main_threat": "none",
            "missed_tactic": False,
        }

        # Check for immediate threats
        for x, y in candidates:
            if Rules.check_winner(board, x, y, role):
                advice["summary"] = "存在必胜策略，优先连接五子"
                advice["main_threat"] = "winning_move"
                break
            if Rules.check_winner(board, x, y, opponent):
                advice["summary"] = "对方存在四连，必须阻断"
                advice["main_threat"] = "opponent_four"
                advice["missed_tactic"] = True
                break

        # Position assessment
        if abs(position_eval) > 10000:
            advantage = "大优" if position_eval > 0 else "劣势"
            advice["summary"] = (
                f"当前局面{advantage}，{'继续进攻' if position_eval > 0 else '需加强防守'}"
            )

        return advice
