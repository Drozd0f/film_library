from datetime import datetime

from src import db
from models.films_genres import films_genres


class Film(db.Model):
    __tablename__ = 'films'

    film_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    genres = db.relationship('Genre', secondary=films_genres, lazy='dynamic', backref='films')
    release_date = db.Column(db.Date)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.director_id', ondelete='SET NULL'))
    director = db.relationship('Director')
    description = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    owner = db.relationship('User')

    def __init__(self, name: str, release_date: datetime, description: str, rating: int,
                 poster: str, director_id: int):
        self.name = name
        self.release_date = release_date
        self.description = description
        self.rating = rating
        self.poster = poster
        self.director_id = director_id

    def __repr__(self):
        return f'<Film(film_id={self.film_id}, director_id={self.director_id}, user_id={self.owner_id})>'
