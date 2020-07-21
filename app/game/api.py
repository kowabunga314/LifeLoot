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
async def read_games(page:int=0, limit:int=100, session:SessionLocal=Depends(get_db)):
    return crud.get_games(session=session)


@router.get("/{game_id}", response_model=Game)
async def get_game(game_id: int, session: SessionLocal = Depends(get_db)):
    return crud.get_game_by_id(session=session, game_id=game_id)


@router.put(
    "/{game_id}",
    response_model=Game
)
async def update_life(game_id:int, state: ScoreUpdate, session: SessionLocal = Depends(get_db)):
    """
    Uses the increment parameter by default, absolute value will be ignored if
        increment is used.
    """
    try:
        game = crud.update_life(state=state, session=session)
    except LookupError:
        raise HTTPException(status_code=404, detail='That game does not exist.')
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.args[0])

    if game:
        session.commit()
        session.refresh(game)
    else:
        raise HTTPException(status_code=400, detail='Failed to update game.')
    
    return game

@router.put('/{game_id}/end', response_model=Game)
async def end_game(game_id: int, session: SessionLocal = Depends(get_db)):
    try:
        game = crud.end_game(game_id=game_id, session=session)
    except LookupError:
        raise HTTPException(status_code=404, detail='That game does not exist.')

    if game:
        session.commit()
        session.refresh(game)
    else:
        raise HTTPException(status_code=400, detail='Failed to update game.')
    
    return game
    