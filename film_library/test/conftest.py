import random
import typing as t
from datetime import date

import pytest
from sqlalchemy.sql.expression import func
from flask.testing import FlaskClient

from src.app import create_app, db
from src.db import database
from src.db.models.users import User
from src.db.models.genres import Genre
from src.db.models.directors import Director
from src.domain.schemes.user import RegistrationUserSchema
from src.domain.schemes.film import RequestFilmSchema


@pytest.fixture(autouse=True)
def set_up():
    # Put code here
    yield


@pytest.fixture(autouse=True)
def teardown():
    yield
    database.cleanup()


@pytest.fixture(scope='module')
def test_client() -> FlaskClient:
    app = create_app(is_tests=True)
    app.app_context().push()
    database.init_db()
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture
def director_factory() -> t.Callable[[int], None]:
    def generate_director(count: int):
        database.director_generate(count)
    return generate_director


@pytest.fixture
def test_user() -> RegistrationUserSchema:
    user = RegistrationUserSchema(
        name='test',
        email='test@gmail.com',
        password1='1'*8,
        password2='1'*8
    )
    database.create_user(user)
    return user


@pytest.fixture
def alternative_test_user() -> RegistrationUserSchema:
    user = RegistrationUserSchema(
        name='test',
        email='testtest@gmail.com',
        password1='1' * 8,
        password2='1' * 8
    )
    database.create_user(user)
    return user


@pytest.fixture
def get_test_user(test_user) -> User:
    return User.get_by_email(test_user.email)


@pytest.fixture
def loging_user(test_user, test_client: FlaskClient) -> RegistrationUserSchema:
    test_client.post(
        '/api/v1/login',
        json={
            'email': test_user.email,
            'password1': test_user.password1
        }
    )
    yield test_user
    test_client.get('/api/v1/logout')


@pytest.fixture
def loging_alternative_user(alternative_test_user, test_client: FlaskClient) -> RegistrationUserSchema:
    test_client.post(
        '/api/v1/login',
        json={
            'email': alternative_test_user.email,
            'password1': alternative_test_user.password1
        }
    )
    yield alternative_test_user
    test_client.get('/api/v1/logout')


@pytest.fixture
def film_factory(get_test_user) -> t.Callable[[int], None]:
    def film_generate(count: int):
        user = get_test_user
        for idx in range(count):
            row_director_id = (
                db.session.query(Director.director_id).
                order_by(func.random()).first()
            )
            director_id = row_director_id['director_id']
            rows_genres_id = (
                db.session.query(Genre.genre_id).
                order_by(func.random()).
                limit(random.randint(1, 3)).all()
            )
            genres_id = [row['genre_id'] for row in rows_genres_id]
            film = RequestFilmSchema(
                name=f'name_{idx}',
                release_date=date.today(),
                description='text',
                rating=random.randint(1, 10),
                poster=f'http://test.test/{idx}',
                genres_id=genres_id,
                director_id=director_id
            ).dict()
            genres = Genre.get_genres(film.pop('genres_id'))
            database.create_film(user, film, genres)
    return film_generate
