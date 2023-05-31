from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.entities.users.user import User

class UserRepository:
    def __init__(self, db_bevflix: AsyncIOMotorDatabase):
        self.users_collection = db_bevflix['Users']

    async def add_user(self, user: User) -> str:
        doc_user = user.to_document()
        result = await self.users_collection.insert_one(doc_user)
        return str(result.inserted_id)
    
    async def get_user(self, id: str) -> User | None:
        doc_user = await self.users_collection.find_one({ '_id': ObjectId(id) })
        print(doc_user)
        if not doc_user:
            return None

        return await self.map_to_user(doc_user)
    
    async def get_user_by_username(self, username: str) -> User | None:
        doc_user = await self.users_collection.find_one({ 'username': username })
        if not doc_user:
            return None

        return await self.map_to_user(doc_user)
    
    async def get_user_by_email(self, email: str) -> User | None:
        doc_user = await self.users_collection.find_one({ 'email': email })
        if not doc_user:
            return None

        return await self.map_to_user(doc_user)

    async def list_users(self) -> list[User]:
        doc_users = await self.users_collection.find().to_list(1000)
        users: list[User] = [await self.map_to_user(doc_user) for doc_user in doc_users]
        return users

    async def update_user(self, user: User) -> bool:
        result = await self.users_collection.update_one({ '_id': ObjectId(user.id) },
                                                        { "$set": { 'username': user.username }})
        return result.modified_count == 1

    async def delete_user(self, id: str) -> bool:
        result = await self.users_collection.delete_one({ '_id': ObjectId(id) })
        return result.deleted_count == 1

    async def map_to_user(self, doc_user: dict):
        return User(
            id=str(doc_user['_id']),
            username=doc_user['username'],
            email=doc_user['email'],
            password=doc_user['password'],
            created_at=doc_user['created_at'],
            updated_at=doc_user['updated_at']
        )
