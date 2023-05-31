import re

from pydantic import BaseModel, Field, validator

from app.configs.errors import BadRequest

class UserLoginRequest(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

    @validator('password')
    def validate_not_null_and_not_empty(cls, value: str):
        if value.strip() == '':
            raise BadRequest(errors={ 'detail': f'password cannot be null or empty'})
        return value
    
    @validator('email')
    def validate_password(cls, value):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, value):
            raise BadRequest(errors={ 'detail': f'invalid email'})
        return value
    
    class Config:
        schema_extra = {
            "example": {
                "email": "le.bevilaqua@gmail.com",
                "password": "pass@123"
            }
        }

class UserLoginResponse(BaseModel):
    access_token: str
    expires_in: int
    token_type: str

