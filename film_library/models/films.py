from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, backref

from config import DataBaseConfig
from models.films_genres import films_genres


class Film(DataBaseConfig.Base):
    __tablename__ = 'films'

    film_id = Column(Integer, primary_key=True)
    genres_id = relationship('Genre', secondary=films_genres, backref=backref('films'))
    release_date = DateTime(timezone=True)
    director_id = Column(Integer, ForeignKey('directors.director_id', ondelete='SET NULL'))
    director = relationship('Director')
    description = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False)
    poster = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship('User')

    def __init__(self, release_date: datetime, description: str, rating: int,
                 poster: str, director_id: int, owner_id: int):
        self.release_date = release_date
        self.description = description
        self.rating = rating
        self.poster = poster
        self.director_id = director_id
        self.owner_id = owner_id

    def __repr__(self):
        return f'<Film(film_id={self.film_id}, director_id={self.director_id}, user_id={self.owner_id})>'
