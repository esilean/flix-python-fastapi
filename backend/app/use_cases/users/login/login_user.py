import logging

from motor.motor_asyncio import AsyncIOMotorDatabase
from passlib.hash import pbkdf2_sha256
from jose import jwt
from datetime import datetime, timedelta

from app.configs.config import Config
from app.configs.errors import BadRequest

from app.use_cases.users.login.schemas.login_user import UserLoginRequest, UserLoginResponse

from app.data.repositories.user import UserRepository


class LoginUserUseCase:
    def __init__(self, db_bevflix: AsyncIOMotorDatabase):
        self.user_repository = UserRepository(db_bevflix)

    async def login_user(self, request: UserLoginRequest) -> UserLoginResponse:
        user = await self.user_repository.get_user_by_email(request.email)
        if not user:
            raise BadRequest(errors= { 'detail': 'invalid email and/or password'})

        authenticated = pbkdf2_sha256.verify(request.password, user.password)
        if not authenticated:
            raise BadRequest(errors= { 'detail': 'invalid email and/or password'})
    
        logging.info(f'generating token for user: {user.username}')

        secret_key = Config.app_settings['credentials']['secret_key']
        expires_at_in_minutes = Config.app_settings['credentials']['expires_at_in_minutes']

        expires_at = datetime.utcnow() + timedelta(minutes=expires_at_in_minutes)
        token_data = {
            'sub': user.username,
            'email': user.email,
            'exp': expires_at,
            'iss': 'bevflix',
            'iat': datetime.now(),
            'claims': [
                'users:get',
                'users:list',
                'users:delete',
                'users:update',
                'admin:health'
            ] if user.username == 'bevila' else []
        }

        access_token = jwt.encode(claims=token_data, key=secret_key, algorithm='HS256')
        expires_in = (expires_at - datetime.utcnow())
        
        return UserLoginResponse(
            access_token=access_token,
            expires_in=expires_in.total_seconds(),
            token_type='bearer'
        )
