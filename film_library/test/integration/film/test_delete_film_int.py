from test.utils import last_film_id
from src.db.models.films import Film
from src.domain.films_dom import delete_film
from src.domain.schemes.film import ResponseFilmSchema


def test_success(loging_user, director_factory, film_factory):
    director_factory(1)
    film_factory(1)
    expected_id = last_film_id()
    film = delete_film(expected_id)
    assert isinstance(film, ResponseFilmSchema)
    assert film.film_id == expected_id
    assert not Film.get(expected_id)
