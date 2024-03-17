from fastapi import APIRouter, HTTPException, Request, Response, Form, status
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse

from models import get_user_or_none, add_user_to_db
from settings import settings
from users.auth import get_password_hash, auth_user, create_access_token
from users.dependencies import get_current_user, get_token
from users.schemas import SUserRegister, SUserLogin

router = APIRouter(
    prefix='/auth',
    tags=['Users / Auth'],
)

templates = Jinja2Templates('templates')


@router.get('/register/')
def create_login(req: Request):
    try:
        user = get_current_user(token=get_token(req))
    except HTTPException:
        user = None
    return templates.TemplateResponse(req, 'register.html', {
        'user': user
    })


@router.post('/register/', response_class=HTMLResponse)
async def reg_user(req: Request, login: str = Form(...), password: str = Form(...)):
    data = SUserRegister(login=login, password=password)
    user_is_exist = get_user_or_none(data.login)
    if user_is_exist:
        return templates.TemplateResponse(req, 'register.html', {
            'user': user_is_exist,
            'error': 'User with this login is already exist'
        })
    hashed_password = get_password_hash(data.password)
    add_user_to_db(data.login, hashed_password, 'user')

    redirect_url = '/auth/login/?message=You have been registered successfully'
    return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)


@router.get('/login/')
def page_login(req: Request, message: str = None):
    try:
        user = get_current_user(token=get_token(req))
    except HTTPException:
        user = None
    return templates.TemplateResponse(req, 'login.html', {
        'user': user,
        'message': message
    })


@router.post('/login/', response_class=HTMLResponse)
def page_login(login: str = Form(...), password: str = Form(...)):
    data = SUserLogin(login=login, password=password)
    user = auth_user(data.login, data.password)

    res = RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)
    
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

    return res


@router.get('/logout/', response_class=HTMLResponse)
def page_logout():
    res = RedirectResponse('/')
    res.delete_cookie(settings.COOKIE_NAME)

    return res