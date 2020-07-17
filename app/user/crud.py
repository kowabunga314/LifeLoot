from sqlalchemy.orm import Session
from . import models, schema
from app.auth.hash import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    try:
        db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    except Exception as e:
        raise e
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user