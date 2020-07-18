"""
This file is used to hash and unhash passwords. It can be used outside
    of the auth package so this functionality is included as its own
    file in order to avoid cyclical imports with other modules.
"""
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)