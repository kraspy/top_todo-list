from fastapi import Depends, Request, HTTPException
from jose import jwt, JWTError

from settings import settings


def get_token(req: Request):
    token = req.cookies.get(settings.COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail='Not authenticated')
    return token


def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
    except JWTError:
        raise HTTPException(status_code=401, detail='Not authenticated')

    user_login = payload.get('sub')

    if not user_login:
        return None

    return user_login
