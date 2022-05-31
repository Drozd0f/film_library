import logging

from sqlalchemy.exc import IntegrityError

from src import db
from models.genres import Genre


log = logging.getLogger(__name__)


def init_db():
    from models import (
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
