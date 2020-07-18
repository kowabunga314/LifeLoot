from typing import List
from fastapi import APIRouter, HTTPException
from app.config import TAGS
from app.game.schema import Game, GameBase

router = APIRouter()


@router.post('/', response_model=Game)
async def create_game(game:GameBase):
    pass

@router.get("/", response_model=List[Game])
async def read_games():
    return [{"name": "Game Foo"}, {"name": "Game Bar"}]


@router.get("/{game_id}", response_model=Game)
async def read_game(game_id: str):
    return {"name": "Fake Specific Game", "game_id": game_id}


@router.put(
    "/{game_id}",
    responses={403: {"description": "Operation forbidden"}},
    response_model=Game
)
async def update_game(game_id: str):
    if game_id != "foo":
        raise HTTPException(status_code=403, detail="You can only update the game: foo")
    return {"game_id": game_id, "name": "The Fighters"}