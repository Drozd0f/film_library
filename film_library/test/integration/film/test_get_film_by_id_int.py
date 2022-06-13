from src.domain.films_dom import get_film_by_id
from src.domain.schemes.film import ResponseFilmSchema
from test.utils import last_film_id


def test_success(director_factory, film_factory):
    director_factory(1)
    film_factory(1)
    expected_id = last_film_id()
    film = get_film_by_id(expected_id)
    assert isinstance(film, ResponseFilmSchema)
    assert film.film_id == expected_id
