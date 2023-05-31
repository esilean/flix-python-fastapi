from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.configs.config import Config
from app.configs.errors import Unauthorized

from app.use_cases.users.get.get_user import GetUserUseCase
from app.use_cases.users.get.schemas.get_user import UserGetUsernameRequest

from app.data.mongo_connection import get_db_bevflix


oauth_scheme = OAuth2PasswordBearer(
    tokenUrl='/auth/login',
    scopes={'users': 'permissions to access users endpoints',
            'admin': 'admin features'}
)

async def get_current_user(token: OAuth2PasswordBearer = Depends(oauth_scheme),
                           db_bevflix: AsyncIOMotorDatabase = Depends(get_db_bevflix)):
    try:
        decoded = jwt.decode(token, Config.app_settings.get('credentials').get('secret_key'), algorithms=['HS256'])
        username = decoded['sub']
        uc = GetUserUseCase(db_bevflix=db_bevflix)
        user = await uc.get_user_by_username(UserGetUsernameRequest(username=username))
        
        return { 
                 "user": user.dict(),
                 "token": decoded
                }
    except JWTError:
        raise Unauthorized(errors={})