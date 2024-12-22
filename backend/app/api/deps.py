from collections.abc import Generator
from typing import Annotated

from app.core.db import engine
from app.services.interfaces import VectorStore
from fastapi import Depends, Request
from sqlmodel import Session


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def get_vector_store(request: Request) -> VectorStore:
    return request.app.state.vector_store

SessionDep = Annotated[Session, Depends(get_db)]
VectorStore = Annotated[object, Depends(get_vector_store)]
