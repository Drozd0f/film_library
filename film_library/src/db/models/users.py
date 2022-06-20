from __future__ import annotations
from werkzeug.security import generate_password_hash

from src.app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password1 = db.Column(db.String(100))
    password2 = db.Column(db.String(100))
    is_staff = db.Column(db.Boolean, default=False)

    def __init__(self, name: str, email: str, password1: str, password2: str):
        self.name = name
        self.email = email
        self.password1 = password1
        self.password2 = password2

    @classmethod
    def create(cls, data: dict) -> User:
        new_user = cls(**data)
        new_user.password1 = generate_password_hash(new_user.password1, method='sha256')
        new_user.password2 = generate_password_hash(new_user.password2, method='sha256')
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def get(cls, id_: int) -> User:
        return db.session.query(cls).filter(cls.user_id == id_).first()

    @classmethod
    def get_by_email(cls, email: str) -> User:
        return (
            db.session.query(cls).
            filter(cls.email == email).
            first()
        )

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f'<User(user_id={self.user_id}, name={self.name}, is_staff={self.is_staff})>'
