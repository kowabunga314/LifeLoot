from app.game.schema import GameCreate, Game
from app.user.schema import UserCreate, UserRead


home_user_create = UserCreate(username='home_team', email='home@bar', password='password')
home_user = UserRead(username='home_team', email='home@bar', id=0, active=True)

away_user_create = UserCreate(username='away_team', email='away@bar', password='password')
away_user = UserRead(username='away_team', email='away@bar', id=0, active=True)
