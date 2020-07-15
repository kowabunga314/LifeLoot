from fastapi import Depends, FastAPI, Header, HTTPException

from .game import api as games
from .user import api as users

app = FastAPI()


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.include_router(users.router)
app.include_router(
    games.router,
    prefix="/games",
    tags=["games"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)