import sqlite3
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel


DATABASE = Path(Path(__file__).parent / 'db' / 'db.sqlite').resolve()


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn


def get_tasks_from_db(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos")
    rows = cur.fetchall()
    conn.close()
    return rows


def add_task_to_db(conn, task):
    sql = '''INSERT INTO todos(text) VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid


def remove_task_from_db(conn, task_id):
    sql = '''DELETE FROM todos WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()


app = FastAPI()
templates = Jinja2Templates('templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

todo_list = [
    'default task'
]


class Task(BaseModel):
    text: str


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
        }
    }

    return templates.TemplateResponse(req, 'index.html', context)


@app.get('/todo/')
def page_todo(req: Request):
    conn = create_connection(DATABASE)
    todo_list = get_tasks_from_db(conn)
    context = {
        'page_title': 'Todos',
        'todos': todo_list
    }

    return templates.TemplateResponse(req, 'todos.html', context)


@app.get('/todo/add_task/')
def add_task(todo: str):
    conn = create_connection(DATABASE)
    add_task_to_db(conn, (todo,))
    conn.close()
    return RedirectResponse('/todo/')


@app.get('/todo/remove_task/')
def remove_task(index: int):
    conn = create_connection(DATABASE)
    remove_task_from_db(conn, index)
    conn.close()
    return RedirectResponse('/todo/')


@app.get('/about/')
def page_todo(req: Request):
    context = {
        'user': {
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
