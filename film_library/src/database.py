import logging

from sqlalchemy.exc import IntegrityError

from config import DataBaseConfig
from models.genres import Genre


log = logging.getLogger(__name__)


def init_db():
    from models import (
        directors, genres, users, films, films_genres
    )
    DataBaseConfig.Base.metadata.create_all(bind=DataBaseConfig.engine)
    try:
        create_genres()
    except IntegrityError:
        log.info('Table genres already exist')


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
    DataBaseConfig.db_session.add_all(genre_name)
    DataBaseConfig.db_session.commit()
