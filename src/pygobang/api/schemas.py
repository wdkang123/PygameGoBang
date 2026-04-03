"""API request/response schemas."""

from typing import List, Optional, Tuple

from pydantic import BaseModel


class NewGameRequest(BaseModel):
    board_size: int = 15
    black_player: str = "human"
    white_player: str = "human"


class MoveRequest(BaseModel):
    x: int
    y: int
    role: int


class StepAnalysisRequest(BaseModel):
    board: List[int]
    current_role: int
    last_move: Optional[Tuple[int, int]] = None
    board_size: int = 15


class ReplayAnalysisRequest(BaseModel):
    replay_id: str


class GameResponse(BaseModel):
    game_id: str
    board: List[int]
    current_role: int
    move_count: int
    winner: Optional[int] = None
    is_over: bool


class MoveResponse(BaseModel):
    success: bool
    x: int
    y: int
    role: int
    winner: Optional[int] = None
    is_over: bool


class StepAnalysisResponse(BaseModel):
    best_move: List[int]
    top_moves: List[List[int]]
    player_move_score: int
    position_eval: int
    phase: str
    advice: dict


class ReplayAnalysisResponse(BaseModel):
    winner: str
    total_moves: int
    critical_moves: List[int]
    blunders: List[int]
    best_alternatives: dict
    style_analysis: dict
    training_suggestions: List[str]
