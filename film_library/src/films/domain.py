import typing as t

from flask import json
from flask_sqlalchemy import BaseQuery

from models.films import Film
from models.users import User
from models.genres import Genre
from models.schemes.film import RequestFilmSchema, ResponseFilmSchema
from models.schemes.paginator import Paginator
from src import database
from src.films import exception
from src.utils import unique_list


def check_film(id_: int, user: t.Optional[User] = None) -> Film:
    film = database.get_film(id_)
    if film is None:
        raise exception.FilmIdNotFoundError
    elif user is not None:
        if film.owner_id != user.user_id or user.is_staff:
            raise exception.UserNotOwnerError
    return film


def check_genres(genres_id: t.List[int]) -> BaseQuery:
    genres_ids = unique_list(genres_id)
    stored_genres = Genre.get_genres(genres_ids)
    if len(genres_ids) != len(stored_genres.all()):
        raise exception.GenresNotMatchError
    return stored_genres


def get_film_by_id(film_id: int) -> ResponseFilmSchema:
    film = check_film(film_id)
    return ResponseFilmSchema.from_orm(film)


def create_film(user: User, data: json) -> ResponseFilmSchema:
    film = RequestFilmSchema(**data).dict()
    genres_id = film.pop('genres_id')
    genres = check_genres(genres_id)
    return ResponseFilmSchema.from_orm(database.create_film(user, film, genres))


def update_film(film_id: int, user: User, data: json) -> ResponseFilmSchema:
    film = RequestFilmSchema(**data).dict()
    check_film(film_id, user)
    genres = check_genres(film.pop('genres_id'))
    updated_film = database.update_film(film_id, film, genres)
    return ResponseFilmSchema.from_orm(updated_film)


def delete_film(film_id: int, user: User) -> ResponseFilmSchema:
    film = ResponseFilmSchema.from_orm(check_film(film_id, user))
    database.delete_film(film_id)
    return film


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
