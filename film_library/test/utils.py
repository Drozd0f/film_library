import random
import typing as t
from datetime import datetime, date

from sqlalchemy.sql.expression import func

from src.app import db
from src.db.models.genres import Genre
from src.db.models.films import Film
from src.db.models.directors import Director


def random_genres_ids() -> t.List[int]:
    rows_genres_id = (
        db.session.query(Genre.genre_id).
        order_by(func.random()).
        limit(random.randint(1, 3)).all()
    )
    return [row['genre_id'] for row in rows_genres_id]


def random_director_id() -> int:
    row_director_id = (
        db.session.query(Director.director_id).
        order_by(func.random()).first()
    )
    return row_director_id['director_id']


def random_film_id() -> int:
    row = db.session.query(Film.film_id).order_by(func.random()).first()
    return row['film_id']


def last_genre_id() -> int:
    id_, = db.session.query(func.max(Genre.genre_id)).first()
    return id_


def last_film_id() -> int:
    id_, = db.session.query(func.max(Film.film_id)).first()
    return id_


def date_dump(date_str: str) -> date:
    return datetime.strptime(date_str, '%Y-%m-%d').date()
