"""Глоссарий должен поддерживать следующие операции:
Получение списка всех терминов.
Получение информации о конкретном термине по ключевому слову.
Добавление нового термина с описанием.
Обновление существующего термина.
Удаление термина из глоссария.
У вас должен применяться Pydantic для валидации входных данных и формирования схем.
Будет плюсом, если вы:
- найдете и используете по назначению инструмент для автоматической генерации статической документации
 с помощью встроенной OpenAPI-спецификации FastAPI;
- реализуйте решение в виде контейнера (Dockerfile) или реализуйте решение с помощью Docker Compose;
- используете для хранения данных  SQLite (или другую легковесную БД);
- обеспечите автоматическую миграцию структуры данных при старте приложения.
"""

from http.client import HTTPException
from typing import Union, Dict
from fastapi import FastAPI
from pydantic import BaseModel
from models import Term, Valute
from utils import DbHandler

app = FastAPI()
db = DbHandler(database_url="sqlite+aiosqlite:///glossary.db")


@app.get("/terms")
async def get_all_terms():
    return db.get_all_terms()


@app.get("/terms/{term}")
async def get_term(term: str):
    if term not in glossary:
        raise HTTPException(status_code=404, detail="Term not found")
    return glossary.get(term, "term not found")


@app.post("/terms/{term}", response_model=Dict[str, Term])
async def post_term(term: str, term_data: Term):
    if term in glossary:
        raise HTTPException(status_code=400, detail="Term already exists!")
    glossary[term] = term_data
    return {term: term_data}


@app.put("/terms/{term}", response_model=Dict[str, Term])
async def change_term(term: str, term_data: Term):
    if term not in glossary:
        raise HTTPException(status_code=400, detail="Term not found!")
    glossary[term] = term_data
    return {term: term_data}


@app.delete("/terms/{term}")
async def delete_term(term: str):
    if term not in glossary:
        raise HTTPException(status_code=404, detail="Term not found!")
    del glossary[term]
    return {"result": "deleted successfully"}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get('/author')
async def read_about():
    from datetime import datetime
    import locale
    locale.setlocale(locale.LC_ALL, 'ru_RU')
    return {'author': "Nick", "datetime": f'{datetime.now().strftime("%A, %d.%m.%Y, %H:%M").title()}'}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


'''@app.get("/valute/{valute_id}")
async def read_valute(valute_id: str):
    return {"valute_id": valute_id}


@app.put("/valute/{valute_id}")
async def update_valute(valute_id: str, _valute: Valute):
    # _valute.name = valute_id
    # _valute.value = 90
    return {"valute_name": _valute.name, "valute_val": _valute.value}

# Создать endpoint, в котором возвращается имя и текущая дата и время по-русски
# {"author": "Nick", "datetime": "Среда, 16.04.2025 12:35"}'''