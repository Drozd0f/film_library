from sqlalchemy import Table, Column, ForeignKey

from config import DataBaseConfig


films_genres = Table(
    'films_genres',
    DataBaseConfig.Base.metadata,
    Column('film_id', ForeignKey('films.film_id')),
    Column('genre_id', ForeignKey('genres.genre_id'))
)
