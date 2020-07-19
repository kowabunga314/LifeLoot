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

def get_games(session: SessionLocal, skip: int = 0, limit: int = 100):
    return session.query(models.Game).offset(skip).limit(limit).all()

def update_life(game: models.Game, state: ScoreUpdate):

    if (state.increment):
        
