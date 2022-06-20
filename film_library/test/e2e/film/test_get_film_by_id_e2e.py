import random
import typing as t

from sqlalchemy.sql.expression import func
from flask.testing import FlaskClient

from src.app import db
from src.db.models.films import Film


def get_random_film_id() -> int:
    row = db.session.query(Film.film_id).order_by(func.random()).first()
    return row['film_id']


def test_success(director_factory: t.Callable[[int], None],
                 film_factory: t.Callable[[int], None], test_client: FlaskClient):
    director_factory(10)
    film_factory(10)
    expected_id = get_random_film_id()
    response = test_client.get(f'/api/v1/films/{expected_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert expected_id == data['film_id']


def test_film_not_exists(test_client):
    response = test_client.get(f'/api/v1/films/{random.randint(1, 10)}')
    assert response.status_code == 404
    data = response.get_json()
    assert 'film don\'t exists' == data['msg']
