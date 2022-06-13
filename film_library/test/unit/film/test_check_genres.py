import random
import typing as t

import pytest
from flask_sqlalchemy import BaseQuery

from src.exception import films_exc
from src.domain.films_dom import check_genres


@pytest.mark.parametrize('genres_ids', [
    [random.randrange(1, 10)] for _ in range(10)
])
def test_success(genres_ids: t.List[int]):
    assert isinstance(check_genres(genres_ids), BaseQuery)


@pytest.mark.parametrize('genres_ids', [
    [random.randrange(11, 21)] for _ in range(10)
])
def test_genres_not_match_error(genres_ids):
    with pytest.raises(films_exc.GenresNotMatchError) as excinfo:
        check_genres(genres_ids)
    assert excinfo.type is films_exc.GenresNotMatchError
