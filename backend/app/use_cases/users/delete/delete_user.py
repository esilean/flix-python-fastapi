from motor.motor_asyncio import AsyncIOMotorDatabase

from app.configs.errors import InternalError, NotFound

from app.use_cases.users.delete.schemas.delete_user import UserDeleteRequest, UserDeleteResponse

from app.data.repositories.user import UserRepository


class DeleteUserUseCase:
    def __init__(self, db_bevflix: AsyncIOMotorDatabase):
        self.user_repository = UserRepository(db_bevflix)

    async def delete_user(self, request: UserDeleteRequest) -> UserDeleteResponse:
        user = await self.user_repository.get_user(id=request.id)
        if not user:
            raise NotFound(errors={ 'detail': 'user not found' })

        deleted = await self.user_repository.delete_user(id=request.id)
        if not deleted:
            raise InternalError(errors={ 'detail': 'error deleting user' })
            
        return UserDeleteResponse()
