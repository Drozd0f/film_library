from src import db


class Genre(db.Model):
    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<Genre(genre_id={self.genre_id}, name={self.name})>'
