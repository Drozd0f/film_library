import pytest

from test.utils import random_genres_ids, random_director_id, last_film_id, date_dump
from src.domain.films_dom import update_film
from src.db.models.films import Film
from src.domain.schemes.film import ResponseFilmSchema
from src.exception.films_exc import FilmNameExist


@pytest.mark.parametrize('data', [
    {
        'name': 'name_1',
        'release_date': '2018-11-11',
        'description': 'jsdadasdas',
        'rating': idx + 1,
        'poster': 'https://test.test'
    }
    for idx in range(10)
])
def test_success(data: dict, loging_user, director_factory, film_factory):
    director_factory(1)
    film_factory(1)
    expected_id = last_film_id()
    data['genres_id'] = random_genres_ids()
    data['director_id'] = random_director_id()
    film = update_film(expected_id, data)
    assert isinstance(film, ResponseFilmSchema)
    assert film.name == data['name']
    assert film.release_date == date_dump(data['release_date'])
    assert film.description == data['description']
    assert film.rating == data['rating']
    assert film.poster == data['poster']
    for genre in film.genres:
        assert genre['id'] in data['genres_id']
    assert film.director['id'] == data['director_id']
    assert Film.get(film.film_id)


@pytest.mark.parametrize('data', [
    {
        'name': 'name_0',
        'release_date': '2018-11-11',
        'description': 'jsdadasdas',
        'rating': idx + 1,
        'poster': 'https://test.test'
    }
    for idx in range(10)
])
def test_film_name_exist(data: dict, loging_user, director_factory, film_factory):
    director_factory(1)
    film_factory(2)
    data['genres_id'] = random_genres_ids()
    data['director_id'] = random_director_id()
    with pytest.raises(FilmNameExist) as excinfo:
        update_film(last_film_id(), data)
    assert excinfo.type is FilmNameExist
