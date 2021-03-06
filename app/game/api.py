from typing import List
from fastapi import APIRouter, HTTPException, Depends
from app.config import TAGS
from app.database import SessionLocal, get_db
from app.auth.crypt import Context
from app.game import crud
from app.game.schema import Game, GameBase, ScoreUpdate

router = APIRouter()


@router.post('/', response_model=Game)
async def new_game(game:GameBase, context: Context = Depends()):
    '''
        Create a new game.
    '''
    new_game = crud.create_game(game)

    if new_game:
        context.session.add(new_game)
        context.session.commit()
        context.session.refresh(new_game)
    else:
        raise HTTPException(status_code=400, detail='Failed to create game.')

    return new_game


@router.get("/mine", response_model=List[Game])
async def my_games(page:int=0, limit:int=100, context: Context = Depends()):
    '''
        Get a list of all games that current user is a part of.
    '''
    return crud.get_games_by_user(user_id=context.agent.id, session=context.session)


@router.get("/{game_id}", response_model=Game)
async def get_game(game_id: int, context: Context = Depends()):
    '''
        Returns game data of game with a matching ID.
    '''
    return crud.get_game_by_id(session=context.session, game_id=game_id)


@router.put(
    "/{game_id}",
    response_model=Game
)
async def update_life(game_id:int, state: ScoreUpdate, context: Context = Depends()):
    """
        Used to manage each player or team's health throughout a game.
        This method uses the increment parameter by default, absolute value 
            will be ignored if increment is used.
    """
    try:
        game = crud.update_life(state=state, session=context.session)
    except LookupError:
        raise HTTPException(status_code=404, detail='That game does not exist.')
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.args[0])

    if game:
        context.session.commit()
        context.session.refresh(game)
    else:
        raise HTTPException(status_code=400, detail='Failed to update game.')
    
    return game


@router.put('/{game_id}/end', response_model=Game)
async def end_game(game_id: int, context: Context = Depends()):
    '''
        Use this method to mark a game as completed.
    '''
    try:
        game = crud.end_game(game_id=game_id, session=context.session)
    except LookupError:
        raise HTTPException(status_code=404, detail='That game does not exist.')

    if game:
        context.session.commit()
        context.session.refresh(game)
    else:
        raise HTTPException(status_code=400, detail='Failed to update game.')
    
    return game
    