from app.database import SessionLocal
from app.game.models import GameModel
from app.game.schema import Game, GameBase, GameCreate
from app.user.models import UserModel
from app.user.schema import UserBase


def create_game(game:GameBase):
    new_game = GameModel(game)
    return new_game
