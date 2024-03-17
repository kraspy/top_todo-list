from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from settings import settings
from models import get_user_or_none
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXP_MIN)
    to_encode.update({
        'exp': expire
    })
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
    )
    return encoded_jwt


def auth_user(login: str, password: str):
    user = get_user_or_none(login)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user