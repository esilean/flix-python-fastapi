import logging

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.use_cases.movies.add.schemas.movie import MovieCreateRequest, MovieCreateResponse

from app.domains.entities.movies.movie import Movie

from app.domains.events.dispatcher import EventDispatcher
from app.domains.events.handler import event_handler
from app.domains.events.movies.movie import MovieCreated

class CreateMovieUseCase:
    def __init__(self, 
                 db_bevflix: AsyncIOMotorDatabase):
        self.db_bevflix = db_bevflix

    @EventDispatcher()
    async def create_movie(self, request: MovieCreateRequest) -> MovieCreateResponse:
        
        newMovie: Movie = Movie.new_movie(request=request)

        await event_handler.store(event=MovieCreated(id=str(newMovie.id), title=newMovie.title))

        return MovieCreateResponse()

        