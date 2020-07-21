from app.database import SessionLocal
from app.game import models
from app.game.schema import Game, GameBase, GameCreate, ScoreUpdate


def create_game(game: GameCreate):
    new_game = models.Game(**game.dict())
    return new_game

def get_game_by_id(session: SessionLocal, game_id: int):
    return session.query(models.Game).filter(models.Game.id == game_id).first()

def get_games_by_user(session: SessionLocal, user_id: int):
    return session.query(models.Game).filter(models.Game.home_id == user_id, models.Game.away_id == user_id).all()

def get_games(session: SessionLocal, page: int = 0, limit: int = 100):
    return session.query(models.Game).offset(page).limit(limit).all()

def update_life(session: SessionLocal, state: ScoreUpdate):
    game = session.query(models.Game).filter(models.Game.id == state.game_id).first()

    # Make sure game was found
    if not game:
        raise LookupError()

    if state.increment:
        if state.team == 'home':
            game.home_life = game.home_life + state.increment
        else:
            game.away_life = game.away_life + state.increment
    else:
        if state.team == 'home':
            game.home_life = state.absolute
        else:
            game.away_life = state.absolute

    return game

def end_game(session: SessionLocal, game_id: int):
    game = session.query(models.Game).filter(models.Game.id == game_id).first()

    # Make sure game was found
    if not game:
        raise LookupError()

    game.active = False
    
    return game
        
