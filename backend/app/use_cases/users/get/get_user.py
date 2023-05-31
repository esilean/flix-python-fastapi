from motor.motor_asyncio import AsyncIOMotorDatabase

from app.configs.errors import NotFound

from app.use_cases.users.get.schemas.get_user import UserGetByIdRequest, UserGetUsernameRequest, UserGetResponse

from app.data.repositories.user import UserRepository


class GetUserUseCase:
    def __init__(self, db_bevflix: AsyncIOMotorDatabase):
        self.user_repository = UserRepository(db_bevflix)

    async def get_user(self, request: UserGetByIdRequest) -> UserGetResponse:
        user = await self.user_repository.get_user(id=request.id)
        if not user:
            raise NotFound(errors={ 'detail': 'user not found' })
            
        return UserGetResponse(
                username=user.username,
                email=user.email
            )
    
    async def get_user_by_username(self, request: UserGetUsernameRequest) -> UserGetResponse:
        user = await self.user_repository.get_user_by_username(username=request.username)
        if not user:
            raise NotFound(errors={ 'detail': 'user not found' })
            
        return UserGetResponse(
                username=user.username,
                email=user.email
            )
