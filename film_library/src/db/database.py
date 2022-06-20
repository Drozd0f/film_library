import logging
import typing as t
from werkzeug.datastructures import ImmutableMultiDict

import names
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import BaseQuery, Pagination

from src.app import db, login_manager
from src.db.filters import with_filter
from src.db.orders import get_order
from src.db.models.genres import Genre
from src.db.models.users import User
from src.db.models.films import Film
from src.db.models.films_genres import films_genres
from src.db.models.directors import Director
from src.domain.schemes.user import RegistrationUserSchema
from src.domain.schemes.film import ResponseFilmSchema
from src.exception.films_exc import FilmNameExist


log = logging.getLogger(__name__)


def init_db():
    from src.db.models import (  # noqa: F401 (Module imported but unused)
        directors, films, films_genres, genres, users
    )
    db.create_all()
    create_genres()


def create_genres():
    genre_name = [
        'Action', 'Comedy',
        'Drama', 'Fantasy',
        'Horror', 'Mystery',
        'Romance', 'Thriller',
        'Western'
    ]
    for idx, name in enumerate(genre_name):
        genre_name[idx] = Genre(name)
    db.session.add_all(genre_name)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        log.info('Table genres already filled')


def create_user(user: RegistrationUserSchema):
    try:
        User.create(user.dict())
    except IntegrityError:
        db.session.rollback()


def create_film(user: User, film: dict, genres: BaseQuery) -> ResponseFilmSchema:
    try:
        return ResponseFilmSchema.from_orm(
            Film.create(user, film, genres)
        )
    except IntegrityError:
        db.session.rollback()
        raise FilmNameExist


def create_director(name: str, surname: str):
    new_director = Director(name=name, surname=surname)
    db.session.add(new_director)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def get_user(user_email: str) -> User:
    return User.get_by_email(user_email)


def get_film(film_id: int) -> t.Optional[ResponseFilmSchema]:
    film = Film.get(film_id)
    if film is not None:
        return ResponseFilmSchema.from_orm(film)


def get_films(query: ImmutableMultiDict, page: int, limit: int) -> t.Tuple[t.List[dict], int]:
    films: Pagination = (
        with_filter(db.session.query(Film), query).
        order_by(get_order(query)).
        paginate(page, limit, False)
    )
    return (
        [ResponseFilmSchema.from_orm(orm_model).dict() for orm_model in films.items],
        films.total
    )


def get_genres(genres_ids: t.List[int]) -> BaseQuery:
    return Genre.get_genres(genres_ids)


def update_film(id_: int, film: dict, genres: BaseQuery) -> ResponseFilmSchema:
    try:
        return ResponseFilmSchema.from_orm(
            Film.update(id_, film, genres)
        )
    except IntegrityError:
        db.session.rollback()
        raise FilmNameExist


def delete_film(id_: int) -> ResponseFilmSchema:
    film = ResponseFilmSchema.from_orm(Film.get(id_))
    Film.delete(id_)
    log.info(f'Film with next parameters was deleted\n{film.dict()}')
    return film


@login_manager.user_loader
def load_user(user_id: int) -> User:
    return db.session.query(User).filter(User.user_id == user_id).one()


def director_generate(count):
    for _ in range(count):
        name = names.get_first_name()
        surname = names.get_last_name()
        create_director(name, surname)


def cleanup():
    tables = (films_genres, Film, User, Director)
    for table in tables:
        db.session.query(table).delete()
    db.session.commit()
