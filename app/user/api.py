from typing import List
from fastapi import APIRouter
from app.user.schema import UserRead

router = APIRouter()


@router.get("/users/", tags=["users"], response_model=List[UserRead])
async def read_users(skip:int=0, offset:int=0):
    return [{"username": "Foo"}, {"username": "Bar"}]


@router.get("/users/me", tags=["users"], response_model=UserRead)
async def read_user_me():
    return {"username": "fakecurrentuser", "email": "foo@bar", "id":"1", "active": True}


@router.get("/users/{username}", tags=["users"], response_model=UserRead)
async def read_user(username: str):
    return {"username": username}