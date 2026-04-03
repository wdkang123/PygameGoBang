"""Integration test: API endpoints — tests API route handlers directly."""

from pygobang.api.routes.analysis import analyze_step
from pygobang.api.routes.game import get_game, make_move, new_game
from pygobang.api.schemas import MoveRequest, NewGameRequest, StepAnalysisRequest


def test_new_game():
    req = NewGameRequest()
    resp = new_game(req)
    assert resp.game_id is not None
    assert resp.current_role == 1  # BLACK
    assert resp.move_count == 0
    assert resp.is_over is False


def test_make_move():
    req = NewGameRequest()
    resp = new_game(req)
    game_id = resp.game_id

    move_req = MoveRequest(x=7, y=7, role=1)
    resp = make_move(game_id, move_req)
    assert resp.success is True
    assert resp.x == 7
    assert resp.y == 7


def test_get_game():
    req = NewGameRequest()
    resp = new_game(req)
    game_id = resp.game_id

    resp = get_game(game_id)
    assert resp.move_count == 0


def test_step_analysis():
    board = [0] * 225
    board[7 * 15 + 7] = 1  # BLACK at center

    req = StepAnalysisRequest(board=board, current_role=2, last_move=[7, 7])
    resp = analyze_step(req)
    assert resp.best_move is not None
    assert resp.position_eval is not None
    assert resp.advice is not None
