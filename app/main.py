from fastapi import Depends, FastAPI, Header, HTTPException
from app.database import get_db
from .auth import api as auth
from .game import api as games
from .user import api as users


app = FastAPI()

async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

class RequestSession():
    def __init__(self):
        self.session = get_db()

# Auth endpoints
app.include_router(auth.router)
# User endpoints
app.include_router(
    users.router,
    prefix="/users"
)
# Game endpoints
app.include_router(
    games.router,
    prefix="/games",
    tags=["games"],
    responses={404: {"description": "Not found"}},
)