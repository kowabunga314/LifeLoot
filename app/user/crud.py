from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from . import models, schema
from app.auth.hash import get_password_hash


def query_users(session: Session, params: schema.UserQuery):
    users = session.query(models.User)

    if params.email is not None: users = users.filter(models.User.email.like(f'%{params.email}%'))
    if params.username is not None: users = users.filter(models.User.username.like(f'%{params.username}%'))
    if params.active is not None: users = users.filter(models.User.active == params.active)

    try:
        users = users.slice(params.page*params.limit, params.limit*params.page+params.limit).all()
    except Exception as e:
        raise e

    return users

def get_user(session: Session, user_id: int):
    return session.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(session: Session, username: str):
    return session.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(session: Session, email: str):
    return session.query(models.User).filter(models.User.email == email).first()


def get_users(session: Session, page: int = 0, limit: int = 100):
    return session.query(models.User).offset(page).limit(limit).all()


def create_user(session: Session, user: schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    if get_user_by_username(session, user.username):
        raise ValueError({'in_use': 'username'})
    if get_user_by_email(session, user.email):
        raise ValueError({'in_use': 'email'})
    try:
        session_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    except Exception as e:
        raise e
    return session_user
