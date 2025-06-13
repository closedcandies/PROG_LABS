from typing import Union
from pydantic import BaseModel


class Valute(BaseModel):
    name: str
    time_n_date: Union[str, None] = ""
    value: float


class Term(BaseModel):
    description: str
    
