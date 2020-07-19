from typing import List
from fastapi import APIRouter, HTTPException, Depends
from app.config import TAGS
from app.database import SessionLocal, get_db
from app.game import crud
from app.game.schema import Game, GameBase, ScoreUpdate

router = APIRouter()


@router.post('/', response_model=Game)
async def new_game(game:GameBase, session:SessionLocal=Depends(get_db)):
    new_game = crud.create_game(game)

    if new_game:
        session.add(new_game)
        session.commit()
        session.refresh(new_game)
    else:
        raise HTTPException(status_code=400, detail='Failed to create game.')

    return new_game

@router.get("/", response_model=List[Game])
async def read_games(skip:int=0, limit:int=100, session:SessionLocal=Depends(get_db)):
    return crud.get_games(session=session)


@router.get("/{game_id}", response_model=Game)
async def get_game(game_id: str, session: SessionLocal = Depends(get_db)):
    return crud.get_game_by_id(session=session, game_id=game_id)


@router.put(
    "/{game_id}",
    responses={403: {"description": "Operation forbidden"}},
    response_model=Game
)
async def update_life(state: ScoreUpdate, session: SessionLocal = Depends(get_db)):
    game = crud.get_game_by_id(session=session, game_id=state.id)

    if not game:
        raise HTTPException(status_code=404, detail='That game does not exist.')

    

    return