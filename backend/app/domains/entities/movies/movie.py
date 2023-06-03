import uuid

from datetime import datetime
from dataclasses import dataclass

from app.use_cases.movies.add.schemas.movie import MovieCreateRequest

@dataclass
class Movie:
    id: str
    title: str
    publication_year: int
    created_at: datetime

    @staticmethod
    def new_movie(request: MovieCreateRequest) -> 'Movie':
        return Movie(id=uuid.uuid4(),
                     title=request.title,
                     publication_year=request.publication_year,
                     created_at=datetime.now())