# -*- coding: utf-8 -*-
# file_name       : main.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2020/8/15 8:37

from typing import Optional

from fastapi import FastAPI
from fastapi import Query

from pydantic import BaseModel

descriptions = "fucking test"

app = FastAPI()


class User(BaseModel):
    name: str
    sex: str
    age: int


@app.post('/user/')
def user(
        user_id: Optional[int] = Query(None, title="fuck you", description="just a test", deprecated=True)
):
    return f"you wanna user: {user_id} \n user info: --->"
