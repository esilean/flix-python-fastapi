from fastapi import APIRouter, status, Depends, Body, Path
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.routes.deps.permissions_checker import PermissionChecker

from app.use_cases.users.signup.schemas.signup_user import UserSignUpRequest, UserSignUpResponse
from app.use_cases.users.list.schemas.list_users import UserListRequest, UserListResponse
from app.use_cases.users.get.schemas.get_user import UserGetByIdRequest, UserGetResponse
from app.use_cases.users.delete.schemas.delete_user import UserDeleteRequest
from app.use_cases.users.update.schemas.update_user import UserUpdateRequest, UserUpdateParamsRequest

from app.use_cases.users.signup.signup_user import SignUpUserUseCase
from app.use_cases.users.list.list_users import ListUsersUseCase
from app.use_cases.users.get.get_user import GetUserUseCase
from app.use_cases.users.delete.delete_user import DeleteUserUseCase
from app.use_cases.users.update.update_user import UpdateUserUseCase

from app.data.mongo_connection import get_db_bevflix


router = APIRouter(prefix='/users', tags=['Users'])

@router.post('/', status_code=status.HTTP_201_CREATED, responses={ 422: {}, 500: {}})
async def signup_user(request: UserSignUpRequest = Body(),
                      db_bevflix: AsyncIOMotorDatabase = Depends(get_db_bevflix)) -> UserSignUpResponse:
    uc = SignUpUserUseCase(db_bevflix=db_bevflix)
    response = await uc.signup_user(request=request)
    return response

@router.get('/', status_code=status.HTTP_200_OK)
async def list_users(__: bool = Depends(PermissionChecker(required_permissions=['users:list'])),
                     db_bevflix: AsyncIOMotorDatabase = Depends(get_db_bevflix)) -> UserListResponse:
    uc = ListUsersUseCase(db_bevflix=db_bevflix)
    response = await uc.list_users(request=UserListRequest())
    return response

@router.get('/{id}', status_code=status.HTTP_200_OK, responses={ 422: {}, 500: {}})
async def get_user(id: str = Path(...), 
                   __: bool = Depends(PermissionChecker(required_permissions=['users:get'])),
                   db_bevflix: AsyncIOMotorDatabase = Depends(get_db_bevflix)) -> UserGetResponse:
    uc = GetUserUseCase(db_bevflix=db_bevflix)
    response = await uc.get_user(request=UserGetByIdRequest(id=id))
    return response

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, responses={ 422: {}, 500: {}})
async def delete_user(id: str = Path(...), 
                      __: bool = Depends(PermissionChecker(required_permissions=['users:delete'])),
                      db_bevflix: AsyncIOMotorDatabase = Depends(get_db_bevflix)):
    uc = DeleteUserUseCase(db_bevflix=db_bevflix)
    await uc.delete_user(request=UserDeleteRequest(id=id))

@router.put('/{id}', status_code=status.HTTP_204_NO_CONTENT, responses={ 422: {}, 500: {}})
async def update_user(id: str = Path(...), 
                      request: UserUpdateRequest = Body(),
                      __: bool = Depends(PermissionChecker(required_permissions=['users:update'])),
                      db_bevflix: AsyncIOMotorDatabase = Depends(get_db_bevflix)):
    uc = UpdateUserUseCase(db_bevflix=db_bevflix)
    await uc.update_user(request=UserUpdateParamsRequest(
        id=id,
        username=request.username
    ))
