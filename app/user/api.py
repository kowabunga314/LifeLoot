from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.user.schema import UserCreate, UserRead
from app.user.crud import create_user, get_users

router = APIRouter()


@router.post("/signup", response_model=UserRead)
async def user_signup(user: UserCreate, session=Depends(get_db)):
    try:
        new_user = create_user(user=user, session=session)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    
    if new_user:
        try:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=e.args[0])
    
    return UserRead(new_user)

@router.get("/", tags=["users"], response_model=List[UserRead])
async def read_users(skip:int=0, limit:int=0, session=Depends(get_db)):
    return get_users(skip=skip, limit=limit, session=session)


@router.get("/me", tags=["users"], response_model=UserRead)
async def read_user_me():
    return {"username": "fakecurrentuser", "email": "foo@bar", "id":"1", "active": True}


@router.get("/{username}", tags=["users"], response_model=UserRead)
async def read_user(username: str):
    return {"username": username}