from fastapi import APIRouter, HTTPException, Request, Response, Form, status
from fastapi.templating import Jinja2Templates

from models import get_user_or_none, add_user_to_db
from settings import settings
from users.auth import get_password_hash, auth_user, create_access_token
from users.schemas import SUserRegister, SUserLogin

router = APIRouter(
    prefix='/auth',
    tags=['Users / Auth'],
)

templates = Jinja2Templates('templates')


@router.get('/register/')
def create_login(req: Request):
    return templates.TemplateResponse(req, 'register.html', {})


@router.post('/register/')
async def reg_user(login: str = Form(...), password: str = Form(...)):
    data = SUserRegister(login=login, password=password)
    user_is_exist = get_user_or_none(data.login)
    if user_is_exist:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='User already exists'
        )
    hashed_password = get_password_hash(data.password)
    add_user_to_db(data.login, hashed_password, 'user')
    return {'message': 'Register success'}


@router.get('/login/')
def page_login(req: Request):
    return templates.TemplateResponse(req, 'login.html', {})


@router.post('/login/')
def page_login(res: Response, login: str = Form(...), password: str = Form(...)):
    data = SUserLogin(login=login, password=password)
    user = auth_user(data.login, data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect login or password'
        )

    access_token = create_access_token({'sub': str(user.login)})
    res.set_cookie(
        settings.COOKIE_NAME,
        access_token,
        httponly=True
    )
    return {'message': 'Login success'}


@router.get('/logout/')
def page_logout(res: Response):
    res.delete_cookie(settings.COOKIE_NAME)
    return {'message': 'Logout success'}