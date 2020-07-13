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
    items: List[Item] = []

    class Config:
        orm_mode = True


class GameBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    home_id: int
    home_life: int = 20
    away_id: int
    away_life: int = 20


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int

    class Config:
        orm_mode = True