from sqlalchemy import Column, Integer, String

from config import DataBaseConfig


class Director(DataBaseConfig.Base):
    __tablename__ = 'directors'

    director_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)

    def __init__(self, name: str, surname: str):
        self.name = name
        self.surname = surname

    def __repr__(self):
        return f'<Director(director_id={self.director_id}, name={self.name}, surname={self.surname})>'
