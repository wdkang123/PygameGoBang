"""Analysis API routes."""

from pathlib import Path
from typing import Dict

from fastapi import APIRouter, HTTPException

from pygobang.ai.advisor import Advisor
from pygobang.api.schemas import (
    ReplayAnalysisRequest,
    ReplayAnalysisResponse,
    StepAnalysisRequest,
    StepAnalysisResponse,
)
from pygobang.core.board import Board
from pygobang.replay.analyzer import ReplayAnalyzer
from pygobang.replay.serializer import Serializer

router = APIRouter(prefix="/analysis", tags=["analysis"])

# In-memory replay store
_replays: Dict[str, Path] = {}

# Singleton advisor
_advisor = Advisor()


@router.post("/step", response_model=StepAnalysisResponse)
def analyze_step(req: StepAnalysisRequest) -> StepAnalysisResponse:
    """Analyze the current position and return advice."""
    board = Board.from_list(req.board, size=req.board_size)
    result = _advisor.analyze(board, req.current_role, req.last_move)
    return StepAnalysisResponse(
        best_move=list(result.best_move),
        top_moves=[list(m) for m in result.top_moves],
        player_move_score=result.player_move_score,
        position_eval=result.position_eval,
        phase=result.phase,
        advice=result.advice,
    )


@router.post("/replay", response_model=ReplayAnalysisResponse)
def analyze_replay(req: ReplayAnalysisRequest) -> ReplayAnalysisResponse:
    """Analyze a saved replay and return structured feedback."""
    replay_path = _replays.get(req.replay_id)
    if not replay_path or not replay_path.exists():
        raise HTTPException(status_code=404, detail=f"Replay {req.replay_id} not found")

    try:
        recorder = Serializer.load(replay_path)
        analyzer = ReplayAnalyzer()
        result = analyzer.analyze(recorder)
        return ReplayAnalysisResponse(
            winner="black" if result.winner == 1 else "white",
            total_moves=result.total_moves,
            critical_moves=result.critical_moves,
            blunders=result.blunders,
            best_alternatives={str(k): list(v) for k, v in result.best_alternatives.items()},
            style_analysis=result.style_analysis,
            training_suggestions=result.training_suggestions,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from None


@router.post("/replay/upload")
def upload_replay(replay_id: str, path: str) -> dict:
    """Register a replay file for analysis."""
    p = Path(path)
    if not p.exists():
        raise HTTPException(status_code=404, detail="Replay file not found")
    _replays[replay_id] = p
    return {"replay_id": replay_id, "status": "registered"}
