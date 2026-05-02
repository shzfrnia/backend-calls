from typing import Generic, TypeVar
from pydantic import BaseModel


T = TypeVar("T")


class BaseWSMessage(BaseModel, Generic[T]):
    type: str
    payload: T
