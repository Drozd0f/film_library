import math
import random
import typing as t
from datetime import date

import pytest
from flask.testing import FlaskClient
from sqlalchemy import func

from src.app import db
from test.utils import date_dump
from src.db.models.directors import Director

COUNT_FILMS = 31


def query_dumps(key: str, value: t.Union[t.List[int], str]) -> str:
    if isinstance(value, str):
        return f'{key}={value}'
    query = ''
    for idx, val in enumerate(value):
        if value[idx] != value[-1]:
            query += f'{key}={val}&'
        else:
            query += f'{key}={val}'
    return query


@pytest.mark.parametrize('page, limit, expected_page, expected_limit, expected_count_films', [
    (None, None, 1, 10, 10),
    (None, 10, 1, 10, 10),
    (1, None, 1, 10, 10),
    (0, 10, 1, 10, 10),
    (2, 1, 2, 1, 1),
    (2, 100, 2, 100, 0),
    (1, 1000000, 1, 100, COUNT_FILMS),
    (1.9, 1.9, 1, 10, 10),
    ('test', 'test', 1, 10, 10)
])
def test_limit_and_page(page: t.Optional[int], limit: t.Optional[int],
                        expected_page: int, expected_limit: int, expected_count_films: int,
                        director_factory: t.Callable[[int], None],
                        film_factory: t.Callable[[int], None],
                        test_client: FlaskClient):
    director_factory(random.randint(4, 10))
    film_factory(COUNT_FILMS)
    response = test_client.get(f'/api/v1/films?page={page}&limit={limit}')
    assert response.status_code == 200
    data = response.get_json()

    assert len(data['films']) == expected_count_films
    assert data['paginator']['page'] == expected_page
    assert data['paginator']['limit'] == expected_limit
    assert data['paginator']['total_pages'] == math.ceil(COUNT_FILMS / expected_limit)


@pytest.mark.parametrize('filters_key, filters_value', [
    ('genres', [2]),
    ('genres', [1]),
    ('genres', [3]),
    ('genres', [1, 3]),
    ('genres', [2, 5])
])
def test_genres(filters_key: str, filters_value: t.List[int],
                director_factory: t.Callable[[int], None],
                film_factory: t.Callable[[int], None],
                test_client: FlaskClient):
    director_factory(random.randint(4, 10))
    film_factory(COUNT_FILMS)
    response = test_client.get(f'/api/v1/films?{query_dumps(filters_key, filters_value)}')
    assert response.status_code == 200

    data = response.get_json()
    for film in data['films']:
        result = []
        for genre_id in filters_value:
            result.extend([genre_id == genre['id'] for genre in film['genres']])
        assert any(result)


@pytest.mark.parametrize('filters_key', [
    'directors', 'directors', 'directors', 'directors', 'directors'
])
def test_directors(filters_key: str,
                   director_factory: t.Callable[[int], None],
                   film_factory: t.Callable[[int], None],
                   test_client: FlaskClient):
    director_factory(random.randint(4, 10))
    film_factory(COUNT_FILMS)

    rows_directors_id = (
        db.session.query(Director.director_id).
        order_by(func.random()).
        limit(random.randint(1, 3)).all()
    )
    directors_id = [row['director_id'] for row in rows_directors_id]

    response = test_client.get(f'/api/v1/films?{query_dumps(filters_key, directors_id)}')
    assert response.status_code == 200

    data = response.get_json()
    for film in data['films']:
        result = []
        for director_id in directors_id:
            result.append(director_id == film['director']['id'])
        assert any(result)


@pytest.mark.parametrize('filters_key, filters_value', [
    ('release_year_range', [date(2012, 12, 4), date(2023, 1, 4)]),
    ('release_year_range', [date(2012, 12, 4), date(2010, 10, 4)]),
    ('release_year_range', [date(2012, 12, 4), date(2010, 10, 4), date(2000, 11, 3)]),
])
def test_release_year_range(filters_key: str, filters_value: list,
                            director_factory: t.Callable[[int], None],
                            film_factory: t.Callable[[int], None],
                            test_client: FlaskClient):
    director_factory(random.randint(4, 10))
    film_factory(COUNT_FILMS)

    response = test_client.get(f'/api/v1/films?{query_dumps(filters_key, filters_value)}')
    assert response.status_code == 200
    data = response.get_json()
    for film in data['films']:
        release_date = date_dump(film['release_date'])
        assert filters_value[0] <= release_date <= filters_value[1]


@pytest.mark.parametrize('filters_key, filters_value, expected_count, limit', [
    ('name', 'name_', COUNT_FILMS, 100),
    ('name', 'name_1', 11, 100),
    ('name', 'name_11', 1, 100),
    ('name', 'name_111', 0, 100)
])
def test_name(filters_key: str, filters_value: list,
              expected_count: int, limit: int,
              director_factory: t.Callable[[int], None],
              film_factory: t.Callable[[int], None],
              test_client: FlaskClient):
    director_factory(random.randint(4, 10))
    film_factory(COUNT_FILMS)

    response = test_client.get(f'/api/v1/films?{query_dumps(filters_key, filters_value)}&limit={limit}')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['films']) == expected_count
