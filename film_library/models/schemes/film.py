import typing as t

from pydantic import BaseModel, conint, HttpUrl

from src.utils import StrictDate


class FilmModelSchema(BaseModel):
    genres_id: t.List[int]
    release_date: StrictDate
    director_id: int
    description: t.Optional[str] = None
    rating: conint(ge=1, le=10)
    poster: HttpUrl
    owner_id: int
