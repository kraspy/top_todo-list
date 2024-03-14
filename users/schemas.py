from pydantic import BaseModel


class SUserRegister(BaseModel):
    login: str
    password: str


class SUserLogin(BaseModel):
    login: str
    password: str
