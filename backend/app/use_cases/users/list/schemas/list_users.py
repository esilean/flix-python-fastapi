from pydantic import BaseModel

class UserListRequest(BaseModel):
    class Config:
        schema_extra = {
            "example": {
            }
        }

class UserListResponseDetail(BaseModel):
    id: str
    username: str
    email: str

class UserListResponse(BaseModel):
    users: list[UserListResponseDetail]

