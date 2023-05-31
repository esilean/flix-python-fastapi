from pydantic import BaseModel, validator, Field
from bson import ObjectId

from app.configs.errors import NotFound

class UserUpdateParamsRequest(BaseModel):
    id: str
    username: str

    @validator('id', 'username')
    def validate_not_null_and_not_empty(cls, value: str):
        if value.strip() == '':
            raise ValueError(f'value cannot be null or empty')
        return value

    @validator('id')
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise NotFound(errors={ 'detail': 'user not found' })
        return value

class UserUpdateRequest(BaseModel):
    username: str

    class Config:
        schema_extra = {
            "example": {
                "username": "bevila"
            }
        }

class UserUpdateResponse(BaseModel):
    pass
