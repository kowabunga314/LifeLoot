from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    active: bool


class User(UserBase):
    id: int
    active: bool
    hashed_password: str

    class Config:
        orm_mode = True
