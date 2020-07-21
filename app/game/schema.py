from typing import List, Optional
from pydantic import BaseModel, validator
from app.user.schema import UserRead


class GameBase(BaseModel):
    home_id: int
    home_life: Optional[int] = 20
    away_id: int
    away_life: Optional[int] = 20
    title: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = True

    class Config:
        orm_mode = True


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int
    home_user: UserRead
    away_user: UserRead

    class Config:
        orm_mode = True


class ScoreUpdate(BaseModel):
    game_id: int
    team: str                   # Can be 'home' or 'away'
    increment: Optional[int]
    absolute: Optional[int]

    # @validator('home', 'away', pre=True)
    # def validate_team(cls, v):
    #     pass
