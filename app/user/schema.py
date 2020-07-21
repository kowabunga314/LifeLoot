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

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    active: bool
    hashed_password: str

    class Config:
        orm_mode = True


# class UserQuery():
#     email: Optional[str] = None
#     username: Optional[str] = None
#     active: Optional[bool] = None
#     page: Optional[int] = 0
#     limit: Optional[int] = 100

class UserQuery:
    def __init__(
        self,
        email: Optional[str] = None,
        username: Optional[str] = None,
        active: Optional[bool] = None,
        page: Optional[int] = 0,
        limit: Optional[int] = 100
    ):
        self.email = email
        self.username = username
        self.active = active
        self.page = page
        self.limit = limit
