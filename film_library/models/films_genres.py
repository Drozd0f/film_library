from src import db


films_genres = db.Table(
    'films_genres',
    db.Column('film_id', db.Integer, db.ForeignKey('films.film_id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.genre_id'))
)
