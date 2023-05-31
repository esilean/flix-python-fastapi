from pydantic import BaseModel, validator
from bson import ObjectId

from app.configs.errors import NotFound, BadRequest

class UserGetByIdRequest(BaseModel):
    id: str

    @validator('id')
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise NotFound(errors={ 'detail': 'user not found' })
        return value

    class Config:
        schema_extra = {
            "example": {
                "id": "6474d6bfdd37f4644528eb57"
            }
        }

class UserGetUsernameRequest(BaseModel):
    username: str

    @validator('username')
    def validate(cls, value):
        if value.strip() == "":
            raise BadRequest(errors={ 'detail': 'username cannot be empty' })
        return value

    class Config:
        schema_extra = {
            "example": {
                "id": "6474d6bfdd37f4644528eb57"
            }
        }

class UserGetResponse(BaseModel):
    username: str
    email: str
