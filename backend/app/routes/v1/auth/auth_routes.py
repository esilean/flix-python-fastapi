from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.routes.deps.get_current_user import get_current_user

from app.use_cases.users.login.schemas.login_user import UserLoginRequest, UserLoginResponse
from app.use_cases.users.login.login_user import LoginUserUseCase

from app.data.mongo_connection import get_db_bevflix


router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/login', status_code=status.HTTP_200_OK, responses={ 400: {}, 500: {} })
async def login_user(request: OAuth2PasswordRequestForm = Depends(),
                     db_bevflix: AsyncIOMotorDatabase = Depends(get_db_bevflix)) -> UserLoginResponse:
    uc = LoginUserUseCase(db_bevflix=db_bevflix)

    response = await uc.login_user(request=UserLoginRequest(
        email=request.username,
        password=request.password
    ))
    return response

@router.post('/me', status_code=status.HTTP_200_OK)
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user['token']
