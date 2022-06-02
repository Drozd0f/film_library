import logging
from werkzeug.security import generate_password_hash

from sqlalchemy.exc import IntegrityError

from src import db, login_manager
from models.genres import Genre
from models.users import User


log = logging.getLogger(__name__)


def init_db():
    from models import (  # noqa: F401 (Module imported but unused)
        directors, films, films_genres, genres, users
    )
    db.create_all()
    try:
        create_genres()
    except IntegrityError:
        log.info('Table genres already filled')


def create_genres():
    genre_name = [
        'Action', 'Comedy',
        'Drama', 'Fantasy',
        'Horror', 'Mystery',
        'Romance', 'Thriller',
        'Western'
    ]
    for idx, name in enumerate(genre_name):
        genre_name[idx] = Genre(name)
    db.session.add_all(genre_name)
    db.session.commit()


def create_user(user):
    new_user = User(
        name=user.name,
        email=user.email,
        password1=generate_password_hash(user.password1, method='sha256'),
        password2=generate_password_hash(user.password2, method='sha256'),
    )
    db.session.add(new_user)
    db.session.commit()


def get_user(user) -> User:
    return db.session.query(User).filter(User.email == user.email).one()


@login_manager.user_loader
def load_user(user_id):  # TODO: create Base model with method (example User.get(id)
    return db.session.query(User).filter(User.user_id == user_id).one()
