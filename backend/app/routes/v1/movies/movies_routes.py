from fastapi import APIRouter, status, Body, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.data.mongo_connection import get_db_bevflix

from app.use_cases.movies.add.schemas.movie import MovieCreateRequest, MovieCreateResponse
from app.use_cases.movies.add.add_movie import CreateMovieUseCase


router = APIRouter(prefix='/movies', tags=['Movies'])

@router.post('/', status_code=status.HTTP_201_CREATED, responses={ 422: {}, 500: {}})
async def create_movie(request: MovieCreateRequest = Body(),
                      db_bevflix: AsyncIOMotorDatabase = Depends(get_db_bevflix)) -> MovieCreateResponse:
    uc = CreateMovieUseCase(db_bevflix=db_bevflix)
    response = await uc.create_movie(request=request)
    return response