from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from app.config import TAGS
from app.database import get_db
from app.auth.crypt import get_current_active_user
from app.user.schema import UserBase, UserCreate, UserRead, User
from app.user.crud import create_user, get_user, get_users

router = APIRouter()


@router.post("/signup", tags=[TAGS.AUTH], response_model=UserRead)
async def user_signup(user: UserCreate, session=Depends(get_db)):
    try:
        new_user = create_user(user=user, session=session)
    except ValueError as e:
        # Email or username already exists
        raise HTTPException(status_code=400, detail=e.args[0])
    
    if new_user:
        try:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        except Exception as e:
            # Something else went wrong while saving user data
            raise HTTPException(status_code=400, detail=e.args[0])
    
    return new_user

@router.get("/", response_model=List[UserRead])
# async def read_users(skip:int=0, limit:int=100, session=Depends(get_db), agent:UserBase = Depends(get_current_active_user)):
async def read_users(skip:int=0, limit:int=100, session=Depends(get_db)):
    return get_users(skip=skip, limit=limit, session=session)


@router.get("/me", response_model=UserRead)
async def read_user_me():
    return {"username": "fakecurrentuser", "email": "foo@bar", "id":"1", "active": True}


@router.get("/{username}", response_model=UserRead)
async def read_user(username: str):
    return {"username": username}

@router.delete("/{user}")
async def delete_user(user: int, session=Depends(get_db)):
    user = get_user(session, user)

    if user:
        session.delete(user)
        session.commit()
    else:
        raise HTTPException(status_code=400, detail='That user does not exist.')
    
    return