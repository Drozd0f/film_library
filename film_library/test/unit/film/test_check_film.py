import random
import typing as t
from dataclasses import dataclass

import pytest
from sqlalchemy.sql.expression import func

from src.app import db
from src.db.models.films import Film
from src.db.models.users import User
from src.domain.schemes.film import ResponseFilmSchema
from src.exception import films_exc
from src.domain.films_dom import check_film
from test.utils import random_film_id


@dataclass
class FakeUser:
    user_id: int
    is_staff: bool


def test_success(director_factory: t.Callable[[int], None], film_factory: t.Callable[[int], None]):
    director_factory(10)
    film_factory(10)
    assert isinstance(check_film(random_film_id()), ResponseFilmSchema)


def test_film_film_id_not_found_error(director_factory: t.Callable[[int], None],
                                      film_factory: t.Callable[[int], None],
                                      get_test_user: User):
    director_factory(10)
    film_factory(10)
    user = random.choice((get_test_user, None))
    film_id, = db.session.query(func.max(Film.film_id)).first()
    with pytest.raises(films_exc.FilmIdNotFoundError) as excinfo:
        check_film(film_id + 1, user)
    assert excinfo.type is films_exc.FilmIdNotFoundError


def test_user_not_owner_error(director_factory: t.Callable[[int], None],
                              get_test_user, film_factory: t.Callable[[int], None]):
    director_factory(10)
    film_factory(10)
    user = FakeUser(user_id=get_test_user.user_id + 1, is_staff=get_test_user.is_staff)
    row = db.session.query(Film.film_id).order_by(func.random()).first()
    film_id = row['film_id']
    with pytest.raises(films_exc.UserNotOwnerError) as excinfo:
        check_film(film_id, user)
    assert excinfo.type is films_exc.UserNotOwnerError
