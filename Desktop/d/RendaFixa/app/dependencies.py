from typing import Annotated
from fastapi import Depends, Request
from app.state import AppState


def get_db(request: Request) -> AppState:
    return request.app.state.db


DB = Annotated[AppState, Depends(get_db)]
