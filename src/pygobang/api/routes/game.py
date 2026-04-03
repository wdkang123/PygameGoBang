"""Game API routes."""

import uuid
from typing import Dict

from fastapi import APIRouter

from pygobang.api.schemas import (
    GameResponse,
    MoveRequest,
    MoveResponse,
    NewGameRequest,
)
from pygobang.core.game import Game

router = APIRouter(prefix="/game", tags=["game"])

# In-memory game store
_games: Dict[str, Game] = {}


@router.post("/new", response_model=GameResponse)
def new_game(req: NewGameRequest) -> GameResponse:
    """Start a new game."""
    game_id = str(uuid.uuid4())[:8]
    game = Game(size=req.board_size)
    _games[game_id] = game
    return GameResponse(
        game_id=game_id,
        board=game.board.to_list(),
        current_role=game.get_current_role(),
        move_count=game.get_move_count(),
        is_over=game.is_over(),
    )


@router.post("/{game_id}/move", response_model=MoveResponse)
def make_move(game_id: str, req: MoveRequest) -> MoveResponse:
    """Place a piece at (x, y)."""
    game = _games.get(game_id)
    if not game:
        return MoveResponse(success=False, x=req.x, y=req.y, role=req.role, is_over=False)

    success = game.make_move(req.x, req.y)
    if not success:
        return MoveResponse(success=False, x=req.x, y=req.y, role=req.role, is_over=game.is_over())

    return MoveResponse(
        success=True,
        x=req.x,
        y=req.y,
        role=req.role,
        winner=game.get_winner(),
        is_over=game.is_over(),
    )


@router.get("/{game_id}", response_model=GameResponse)
def get_game(game_id: str) -> GameResponse:
    """Get current game state."""
    game = _games.get(game_id)
    if not game:
        raise ValueError(f"Game {game_id} not found")
    return GameResponse(
        game_id=game_id,
        board=game.board.to_list(),
        current_role=game.get_current_role(),
        move_count=game.get_move_count(),
        winner=game.get_winner(),
        is_over=game.is_over(),
    )
