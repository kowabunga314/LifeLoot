from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from .crypt import authenticate_user, get_current_active_user, create_access_token
from .hash import verify_password, get_password_hash
from .schema import Token, TokenData
from app.config import TAGS, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import SessionLocal, get_db
from app.user.schema import UserBase, UserCreate
from app.user.crud import get_user, get_user_by_username



# Create router
router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: SessionLocal = Depends(get_db)):
    '''
        Request an access token to authenticate user. Based off of OAuth2 password flow.
            Returns JWT to be sent as a bearer for authenticated requests.
    '''
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})

    # TODO: Add refresh tokens to authentication header

    return {"access_token": access_token, "token_type": "bearer"}
