from pydantic import BaseModel

class MovieCreateRequest(BaseModel):
    title: str
    publication_year: int

class MovieCreateResponse(BaseModel):
    ...