from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from rich import inspect, print

from models import get_tasks_from_db, add_task_to_db, remove_task_from_db, User
from users.dependencies import get_current_user
from users.router import router as users_router

app = FastAPI()

app.include_router(users_router)

templates = Jinja2Templates('templates')
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/')
def index(req: Request):
    context = {
        'page_title': 'Home',
        'content': {
            'py_types': {
                'str': 'some string',
                'int': 123,
                'tuple': (1, 2, 3),
                'list': [1, 2, 3],
                'dict': {'a': 1, 'b': 2}
            }
        },
    }

    return templates.TemplateResponse(req, 'index.html', context)


@app.get('/todo/')
def page_todo(req: Request, user: User = Depends(get_current_user)):
    todo_list = get_tasks_from_db()
    context = {
        'page_title': 'Todos',
        'todos': todo_list,
        'user': user,
    }

    return templates.TemplateResponse(req, 'todos.html', context)


@app.post('/todo/add_task/')
def add_task(todo: str = Form(...)):
    add_task_to_db(todo)
    return RedirectResponse('/todo/', status_code=303)


@app.post('/todo/remove_task/')
def remove_task(index: str = Form(...)):
    remove_task_from_db(index)
    return RedirectResponse('/todo/', status_code=303)


@app.get('/about/')
def page_about(req: Request):
    context = {
        'info': {
            'name': 'Evgeniy',
            'code_lang': 'Python',
            'email': 'kraspy@yandex.ru',
            'github': 'https://github.com/kraspy',
            'skills': {
                'languages': [
                    'HTML/CSS/JS',
                    'Python',
                ],
                'technologies': [
                    'Git',
                    'Github',
                    'SQL',
                ],
                'frameworks': [
                    'Bootstrap 5',
                    'FastAPI',
                    'Django',
                ],
            },
        },
    }
    print(context)
    return templates.TemplateResponse(req, 'about.html', context)


