from sqlalchemy import Column, Integer, String, Boolean

from config import DataBaseConfig


class User(DataBaseConfig.Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    is_staff = Column(Boolean, default=False)

    def __init__(self, name: str, surname: str, is_staff: bool = False):
        self.name = name
        self.surname = surname
        self.is_staff = is_staff

    def __repr__(self):
        return f'<User(user_id={self.user_id}, name={self.name}, ' \
               f'surname={self.surname}, is_staff={self.is_staff})>'
