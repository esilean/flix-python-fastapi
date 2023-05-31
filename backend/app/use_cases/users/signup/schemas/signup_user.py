from pydantic import BaseModel, Field, validator, EmailStr

class UserSignUpRequest(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    @validator('username', 'email', 'password')
    def validate_not_null_and_not_empty(cls, value: str):
        if value.strip() == '':
            raise ValueError(f'value cannot be null or empty')
        return value

    @validator('password')
    def validate_password(cls, value):
        return value
    
    class Config:
        schema_extra = {
            "example": {
                "username": "bevila",
                "email": "le.bevilaqua@gmail.com",
                "password": "pass@123"
            }
        }

class UserSignUpResponse(BaseModel):
    id: str

