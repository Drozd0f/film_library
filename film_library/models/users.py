from flask_login import UserMixin

from src import db


class User(UserMixin, db.Model):
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

    def __repr__(self):
        return f'<User(user_id={self.user_id}, name={self.name}, is_staff={self.is_staff})>'
