from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import create_engine, select

# DATABASE SETTINGS
DB_URL = 'sqlite:///db/todo.db'


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(10))

    def __str__(self):
        return f'{self.id} - {self.login}'

    def __repr__(self):
        return f'User(id={self.id}, username="{self.login}")'


class Todo(Base):
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(100))
    done: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    def __str__(self):
        return f'{self.id} - {self.text}'

    def __repr__(self):
        return f'Todo(id={self.id}, text="{self.text}", done={self.done})'


engine = create_engine(DB_URL, echo=True)

Base.metadata.create_all(engine)


# DATABASE FUNCTIONS
def get_tasks_from_db():
    with Session(engine) as session:
        tasks = session.scalars(select(Todo)).all()
        return tasks


def add_task_to_db(task):
    with Session(engine) as session:
        todo = Todo(text=task, done=False)
        session.add(todo)
        session.commit()


def update_task_in_db(todo_id, text):
    with Session(engine) as session:
        task = session.get(Todo, int(todo_id))
        task.text = text
        session.commit()


def remove_task_from_db(todo_id):
    try:
        todo_id = int(todo_id)
    except ValueError:
        return
    with Session(engine) as session:
        task = session.get(Todo, todo_id)
        session.delete(task)
        session.commit()


# USERS FUNCTIONS
def get_user_or_none(login):
    with Session(engine) as session:
        user = session.scalars(
            select(User).where(User.login == login)).first()
        return user


def add_user_to_db(login, hashed_password, role):
    with Session(engine) as session:
        user = User(
            login=login,
            hashed_password=hashed_password,
            role=role
        )
        session.add(user)
        session.commit()
