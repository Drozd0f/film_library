import typing as t
from werkzeug.datastructures import ImmutableMultiDict

from flask import json
from flask_login import current_user
from flask_login.utils import LocalProxy
from flask_sqlalchemy import BaseQuery

from src.db import database
from src.domain.schemes.paginator import Paginator
from src.domain.schemes.film import RequestFilmSchema, ResponseFilmSchema
from src.exception import films_exc
from src.utils import unique_list


def check_film(id_: int, user: t.Optional[LocalProxy] = None) -> t.Optional[ResponseFilmSchema]:
    film = database.get_film(id_)
    if film is None:
        raise films_exc.FilmIdNotFoundError
    if user is not None:
        if film.owner['id'] != user.user_id and not user.is_staff:
            raise films_exc.UserNotOwnerError
    return film


def check_genres(genres_id: t.List[int]) -> BaseQuery:
    genres_ids = unique_list(genres_id)
    stored_genres = database.get_genres(genres_ids)
    if len(genres_ids) != len(stored_genres.all()):
        raise films_exc.GenresNotMatchError
    return stored_genres


def get_film_by_id(film_id: int) -> ResponseFilmSchema:
    return check_film(film_id)


def create_film(data: json) -> ResponseFilmSchema:
    film = RequestFilmSchema(**data).dict()
    genres_id = film.pop('genres_id')
    genres = check_genres(genres_id)
    return database.create_film(current_user, film, genres)


def update_film(film_id: int, data: json) -> ResponseFilmSchema:
    film = RequestFilmSchema(**data).dict()
    check_film(film_id, current_user)
    genres = check_genres(film.pop('genres_id'))
    return database.update_film(film_id, film, genres)


def delete_film(film_id: int) -> ResponseFilmSchema:
    check_film(film_id, current_user)
    return database.delete_film(film_id)


def get_films(query: ImmutableMultiDict) -> dict:
    paginator = Paginator(
        query.get('page', '1'),
        query.get('limit', '10')
    )
    films, count_films = database.get_films(query, paginator.page, paginator.limit)
    paginator.total_pages = count_films
    return {
        'films': films,
        'paginator': paginator.to_dict()
    }
