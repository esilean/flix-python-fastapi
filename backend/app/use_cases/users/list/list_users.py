from motor.motor_asyncio import AsyncIOMotorDatabase

from app.domains.entities.users.user import User

from app.use_cases.users.list.schemas.list_users import UserListRequest, UserListResponse, UserListResponseDetail

from app.data.repositories.user import UserRepository


class ListUsersUseCase:
    def __init__(self, db_bevflix: AsyncIOMotorDatabase):
        self.user_repository = UserRepository(db_bevflix)

    async def list_users(self, request: UserListRequest) -> UserListResponse:
        users: list[User] = await self.user_repository.list_users()
        if not users:
            return UserListResponse(users=[])
            
        users_details: list[UserListResponseDetail] = []
        for user in users:
            users_details.append(UserListResponseDetail(
                id=user.id,
                username=user.username,
                email=user.email
            ))

        return UserListResponse(users=users_details)
