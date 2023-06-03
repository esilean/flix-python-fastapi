import uuid

from bson import ObjectId
from pydantic import BaseModel, Field, validator
from datetime import datetime

from app.data.mongo_model import MongoModel


class User(MongoModel, BaseModel):
    id: str = Field(default_factory=uuid.uuid4)
    username: str = Field(...)
    email: str = Field(...)
    image: str = Field(...)
    password: str = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

    @validator('id')
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError('invalid id')
        return value

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = { uuid.uuid4: str }