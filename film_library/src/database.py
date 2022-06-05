import logging
import typing as t
from werkzeug.security import generate_password_hash

from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import BaseQuery

from src import db, login_manager
from src.filters import filter_generator
from src.orders import get_order
from models.genres import Genre
from models.users import User
from models.films import Film
from models.schemes.user import RegistrationUserSchema, LoginUserSchema


log = logging.getLogger(__name__)


def init_db():
    from models import (  # noqa: F401 (Module imported but unused)
        directors, films, films_genres, genres, users
    )
    db.create_all()
    try:
        create_genres()
    except IntegrityError:
        log.info('Table genres already filled')


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
    db.session.commit()


def create_user(user: RegistrationUserSchema):
    new_user = User(
        name=user.name,
        email=user.email,
        password1=generate_password_hash(user.password1, method='sha256'),
        password2=generate_password_hash(user.password2, method='sha256'),
    )
    db.session.add(new_user)
    db.session.commit()


def create_film(user: User, film: dict, genres: BaseQuery):
    new_film = Film(**film)
    new_film.owner_id = user.user_id
    new_film.genres.extend(genres)
    db.session.add(new_film)
    db.session.commit()


def get_user(user: LoginUserSchema) -> User:
    return db.session.query(User).filter(User.email == user.email).one()


def get_films(query, page: int, limit: int) -> t.Tuple[t.List[Film], int]:
    films = Film.query.join(Film.genres).filter(*filter_generator(query))
    total_count = films.count()
    current_page = (page - 1) * limit
    films = films.order_by(get_order(query)).limit(limit).offset(current_page).all()
    return films, total_count


@login_manager.user_loader
def load_user(user_id):  # TODO: create Base model with method (example User.get(id))
    return db.session.query(User).filter(User.user_id == user_id).one()
