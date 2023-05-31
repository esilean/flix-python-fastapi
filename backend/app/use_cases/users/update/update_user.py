
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.configs.errors import NotFound, InternalError, BadRequest

from app.use_cases.users.update.schemas.update_user import UserUpdateParamsRequest, UserUpdateResponse

from app.data.repositories.user import UserRepository


class UpdateUserUseCase:
    def __init__(self, db_bevflix: AsyncIOMotorDatabase):
        self.user_repository = UserRepository(db_bevflix)

    async def update_user(self, request: UserUpdateParamsRequest) -> UserUpdateResponse:
        user = await self.user_repository.get_user(id=request.id)
        if not user:
            raise NotFound(errors={ 'detail': 'user not found' })

        if user.username == request.username:
            return UserUpdateResponse()
        
        username_exists = await self.user_repository.get_user_by_username(request.username)
        if username_exists:
            raise BadRequest(errors= { 'detail': 'username already taken'})

        user.username = request.username
        updated = await self.user_repository.update_user(user=user)
        if not updated:
            raise InternalError(errors={ 'detail': 'error updating user' })

        return UserUpdateResponse()
