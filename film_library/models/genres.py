from sqlalchemy import Column, Integer, String, Boolean

from config import DataBaseConfig


class Genre(DataBaseConfig.Base):
    __tablename__ = 'genres'

    genre_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<Genre(genre_id={self.genre_id}, name={self.name})>'
