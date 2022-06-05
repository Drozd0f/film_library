import typing as t

from flask import json

from models.films import Film
from models.users import User
from models.genres import Genre
from models.schemes.film import RequestFilmSchema, ResponseFilmSchema
from models.schemes.paginator import Paginator
from src import database
from src.films.exception import GenresNotMatchError
from src.utils import unique_list


def create_film(user: User, data: json):
    film = RequestFilmSchema(**data).dict()
    genres_ids = unique_list(film.pop('genres_id'))
    stored_genres = Genre.get_genres(genres_ids)
    if len(genres_ids) != len(stored_genres.all()):
        raise GenresNotMatchError
    database.create_film(user, film, stored_genres)


def convert_orm_to_pydent_dict(orm_models: t.List[Film]) -> t.List[dict]:
    return [ResponseFilmSchema.from_orm(orm_model).dict() for orm_model in orm_models]


def get_films(query: dict) -> dict:
    paginator = Paginator(
        query.get('page', '1'),
        query.get('limit', '10')
    )
    films, count_films = database.get_films(query, paginator.page, paginator.limit)
    paginator.total_pages = count_films
    return {
        'films': convert_orm_to_pydent_dict(films),
        'paginator': paginator.to_dict()
    }
