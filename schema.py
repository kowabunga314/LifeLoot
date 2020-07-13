from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class GameBase(BaseModel):
    home_id: int
    home_user: User
    home_life: int = 20
    away_id: int
    away_user: User
    away_life: int = 20
    title: Optional[str] = None
    description: Optional[str] = None
    active: bool = True


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int

    class Config:
        orm_mode = True