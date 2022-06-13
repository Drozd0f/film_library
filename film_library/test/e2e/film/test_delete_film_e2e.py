from flask.testing import FlaskClient

from src.domain.schemes.user import RegistrationUserSchema
from test.utils import last_film_id


def test_success(director_factory, film_factory,
                 loging_user: RegistrationUserSchema, test_client: FlaskClient):
    director_factory(1)
    film_factory(1)
    expected_id = last_film_id()
    response = test_client.delete(f'/api/v1/films/{expected_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['film_id'] == expected_id


def test_film_not_found(director_factory, film_factory,
                        loging_user: RegistrationUserSchema, test_client: FlaskClient):
    director_factory(1)
    film_factory(1)
    response = test_client.delete(f'/api/v1/films/{last_film_id() + 1}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['msg'] == 'film don\'t exists'


def test_user_not_owner(director_factory, film_factory,
                        loging_alternative_user: RegistrationUserSchema, test_client: FlaskClient):
    director_factory(1)
    film_factory(1)
    film_id = last_film_id()
    response = test_client.delete(f'/api/v1/films/{film_id}')
    assert response.status_code == 403
    data = response.get_json()
    assert data['msg'] == 'permission denied'
    test_client.get('/api/v1/logout')
