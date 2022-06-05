import typing as t
from datetime import date

from pydantic import BaseModel, conint, constr, HttpUrl, validator


class BaseFilmSchema(BaseModel):
    name: constr(max_length=255)
    release_date: date
    description: t.Optional[str] = None
    rating: conint(ge=1, le=10)
    poster: HttpUrl


class RequestFilmSchema(BaseFilmSchema):
    genres_id: t.List[int]
    director_id: int


class ResponseFilmSchema(BaseFilmSchema):
    film_id: int
    genres: t.List[dict]
    director: t.Dict[str, t.Any]
    owner: t.Dict[str, t.Any]

    @validator('genres', pre=True, check_fields=False)
    def evaluate_genres(cls, v):
        genres = v.all()
        return [{'id': genre.genre_id, 'name': genre.name} for genre in genres]

    @validator('director', pre=True, check_fields=False)
    def evaluate_director(cls, v):
        return {
            'id': v.director_id,
            'name': v.name,
            'surname': v.surname
        }

    @validator('owner', pre=True, check_fields=False)
    def evaluate_owner(cls, v):
        return {
            'id': v.user_id,
            'name': v.name,
            'is_staff': v.is_staff
        }

    class Config:
        orm_mode = True
