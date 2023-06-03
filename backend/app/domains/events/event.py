from abc import ABC
from pydantic import BaseModel


class BaseEvent(ABC, BaseModel):
    ...