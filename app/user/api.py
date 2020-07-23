from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from app.config import TAGS
from app.database import get_db, SessionLocal
from app.auth.crypt import Context
from app.user.schema import UserBase, UserCreate, UserRead, User, UserQuery
from app.user.crud import create_user, query_users, get_user, get_users, get_user_by_username


router = APIRouter()

@router.post("/signup", tags=[TAGS.AUTH], response_model=UserRead)
async def user_signup(user: UserCreate, session:SessionLocal=Depends(get_db)):
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

@router.get("/search", response_model=List[UserRead])
async def search_users(params: UserQuery = Depends(), context: Context = Depends()):
    try:
        users = query_users(params=params, session=context.session)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.args[0])

    return users

@router.get("/", response_model=List[UserRead])
# async def read_users(page:int=0, limit:int=100, session=Depends(get_db)):
async def read_users(page: int = 0, limit: int = 100, context: Context = Depends()):
    return get_users(page=page, limit=limit, session=context.session)


@router.get("/me", response_model=UserRead)
async def read_user_me():
    return {"username": "fakecurrentuser", "email": "foo@bar", "id":"1", "active": True}


@router.get("/{username}", response_model=UserRead)
async def read_user(username: str, session:SessionLocal=Depends(get_db)):
    user =  get_user_by_username(session=session, username=username)

    if not user:
        raise HTTPException(status_code=404, detail='User not found.')
    else:
        return user

@router.delete("/{user}")
async def delete_user(user:int, session:SessionLocal=Depends(get_db)):
    user = get_user(session, user)

    if user:
        session.delete(user)
        session.commit()
    else:
        raise HTTPException(status_code=400, detail='That user does not exist.')
    
    return