from src.app import db


class Director(db.Model):
    __tablename__ = 'directors'

    director_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)

    def __init__(self, name: str, surname: str):
        self.name = name
        self.surname = surname

    def __repr__(self):
        return f'<Director(director_id={self.director_id}, name={self.name}, surname={self.surname})>'
