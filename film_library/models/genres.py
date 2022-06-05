from flask_sqlalchemy import BaseQuery

from src import db


class Genre(db.Model):
    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name: str):
        self.name = name

    @classmethod
    def get_genres(cls, genres_ids: list) -> BaseQuery:
        return cls.query.filter(cls.genre_id.in_(genres_ids))

    def __repr__(self):
        return f'<Genre(genre_id={self.genre_id}, name={self.name})>'
