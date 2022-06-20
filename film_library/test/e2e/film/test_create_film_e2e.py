import typing as t

import pytest
from flask.testing import FlaskClient

from src.domain.schemes.user import RegistrationUserSchema
from test.utils import random_genres_ids, random_director_id, last_genre_id


@pytest.mark.parametrize('data', [
    {
        'name': f'Test {idx}',
        'release_date': '2018-11-11',
        'description': 'jsdadasdas',
        'rating': idx + 1,
        'poster': 'https://test.test'
    }
    for idx in range(10)
])
def test_success(data: dict, director_factory, loging_user: RegistrationUserSchema, test_client: FlaskClient):
    director_factory(10)
    data['genres_id'] = random_genres_ids()
    data['director_id'] = random_director_id()
    response = test_client.post('/api/v1/films', json=data)
    assert response.status_code == 201

    resp_data = response.get_json()
    assert resp_data['name'] == data['name']
    assert resp_data['release_date'] == data['release_date']
    assert resp_data['description'] == data['description']
    assert resp_data['rating'] == data['rating']
    assert resp_data['poster'] == data['poster']
    for genre in resp_data['genres']:
        assert genre['id'] in data['genres_id']
    assert resp_data['director']['id'] == data['director_id']


@pytest.mark.parametrize('data', [
    {
        'name': f'name_{idx}',
        'release_date': '2018-11-11',
        'description': 'jsdadasdas',
        'rating': idx + 1,
        'poster': 'https://test.test'
    }
    for idx in range(10)
])
def test_user_unauthorized(data: dict, director_factory, test_client: FlaskClient):
    director_factory(1)
    data['genres_id'] = random_genres_ids()
    data['director_id'] = random_director_id()
    response = test_client.post('/api/v1/films', json=data)
    assert response.status_code == 401
    resp_data = response.get_json()
    assert resp_data['msg'] == 'user unauthorized'


@pytest.mark.parametrize('data, expected_loc, expected_msg, expected_type', [
    (
            {
                'genres_id': [1, 2],
                'name': 'test' * 250,
                'release_date': '2018-11-11' * 2,
                'rating': 1,
                'director_id': 1,
                'poster': 'test.test'
            },
            ('name', 'release_date', 'poster'),
            ('ensure this value has at most 255 characters', 'invalid date format', 'invalid or missing URL scheme'),
            ('value_error.any_str.max_length', 'value_error.date', 'value_error.url.scheme')
    ),
    (
            {
                'genres_id': ['1', '2'],
                'release_date': '2018-11-11',
                'rating': 1,
                'poster': 'https://test.test'
            },
            ('name', 'director_id'),
            ('field required', 'field required'),
            ('value_error.missing', 'value_error.missing')
    ),
    (
            {
                'genres_id': [1, 2],
                'name': 'test',
                'release_date': '2018-11-11',
                'rating': 1,
                'director_id': '1',
                'poster': 'test.test'
            },
            ('poster',),
            ('invalid or missing URL scheme',),
            ('value_error.url.scheme',)
    ),
    (
            {
                'genres_id': [1, 2],
                'name': 'test',
                'release_date': '2018-11-11',
                'rating': 11,
                'director_id': 1,
                'poster': 'https://test.test'
            },
            ('rating',),
            ('ensure this value is less than or equal to 10',),
            ('value_error.number.not_le',)
    ),
    (
            {
                'genres_id': [1, 2],
                'name': 'test',
                'release_date': '2018-11-11',
                'rating': 0,
                'director_id': 1,
                'poster': 'https://test.test'
            },
            ('rating',),
            ('ensure this value is greater than or equal to 1',),
            ('value_error.number.not_ge',)
    ),

])
def test_validate_error(data: dict, expected_loc: t.Tuple[str],
                        expected_msg: t.Tuple[str], expected_type: t.Tuple[str],
                        loging_user: RegistrationUserSchema, test_client: FlaskClient):
    response = test_client.post('/api/v1/films', json=data)

    data = response.get_json()
    assert response.status_code == 400
    for idx, info in enumerate(data['msg']):
        if expected_loc[idx] is not None:
            assert info['loc'][0] == expected_loc[idx]
        assert info['msg'] == expected_msg[idx]
        assert info['type'] == expected_type[idx]


@pytest.mark.parametrize('data', [
    {
        'name': f'name_{idx}',
        'release_date': '2018-11-11',
        'description': 'jsdadasdas',
        'rating': idx + 1,
        'poster': 'https://test.test'
    }
    for idx in range(10)
])
def test_name_exist(data: dict, director_factory, film_factory,
                    loging_user: RegistrationUserSchema, test_client: FlaskClient):
    director_factory(10)
    film_factory(10)
    data['genres_id'] = random_genres_ids()
    data['director_id'] = random_director_id()
    response = test_client.post('/api/v1/films', json=data)
    assert response.status_code == 409
    resp_data = response.get_json()
    assert resp_data['msg'] == 'film with this name already exists'


@pytest.mark.parametrize('data', [
    {
        'name': f'name_{idx}',
        'release_date': '2018-11-11',
        'description': 'jsdadasdas',
        'rating': idx + 1,
        'poster': 'https://test.test'
    }
    for idx in range(10)
])
def test_unknown_genres_ids(data: dict, director_factory, film_factory,
                            loging_user: RegistrationUserSchema, test_client: FlaskClient):
    director_factory(10)
    data['genres_id'] = [last_genre_id() + 1]
    data['director_id'] = random_director_id()
    response = test_client.post('/api/v1/films', json=data)
    assert response.status_code == 400
    resp_data = response.get_json()
    assert resp_data['msg'] == 'unknown genres ids'
