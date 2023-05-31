import logging

from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from passlib.hash import pbkdf2_sha256

from app.configs.errors import BadRequest

from app.entities.users.user import User
from app.use_cases.users.signup.schemas.signup_user import UserSignUpRequest, UserSignUpResponse

from app.data.repositories.user import UserRepository


class SignUpUserUseCase:
    def __init__(self, db_bevflix: AsyncIOMotorDatabase):
        self.user_repository = UserRepository(db_bevflix)

    async def signup_user(self, request: UserSignUpRequest) -> UserSignUpResponse:
        username_exists = await self.user_repository.get_user_by_username(request.username)
        if username_exists:
            raise BadRequest(errors= { 'detail': 'username already taken'})
        
        email_exists = await self.user_repository.get_user_by_email(request.email)
        if email_exists:
            raise BadRequest(errors= { 'detail': 'email already taken'})

        password_hashed = pbkdf2_sha256.hash(request.password)
        user = User(
            username=request.username,
            email=request.email,
            password=password_hashed,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        logging.info(f'User: {user.dict()}')

        user_id = await self.user_repository.add_user(user)

        return UserSignUpResponse(id=user_id)
