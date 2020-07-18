from sqlalchemy.orm import Session
from . import models, schema
from app.auth.hash import get_password_hash


def get_user(session: Session, user_id: int):
    return session.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(session: Session, username: str):
    return session.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(session: Session, email: str):
    return session.query(models.User).filter(models.User.email == email).first()


def get_users(session: Session, skip: int = 0, limit: int = 100):
    return session.query(models.User).offset(skip).limit(limit).all()


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