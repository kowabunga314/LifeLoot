from typing import List
from fastapi import APIRouter, Depends
from app.database import get_db
from app.user.schema import UserCreate, UserRead
from app.user.crud import create_user

router = APIRouter()


@router.post("/signup", response_model=UserRead)
async def user_signup(user: UserCreate, session=Depends(get_db)):
    try:
        new_user = create_user(user=user, db=session)
    except Exception as e:
        raise e
    
    if new_user:
        session.add(new_user)
        session.commit()
    
    return UserRead(new_user)

@router.get("/", tags=["users"], response_model=List[UserRead])
async def read_users(skip:int=0, offset:int=0):
    return [{"username": "Foo"}, {"username": "Bar"}]


@router.get("/me", tags=["users"], response_model=UserRead)
async def read_user_me():
    return {"username": "fakecurrentuser", "email": "foo@bar", "id":"1", "active": True}


@router.get("/{username}", tags=["users"], response_model=UserRead)
async def read_user(username: str):
    return {"username": username}