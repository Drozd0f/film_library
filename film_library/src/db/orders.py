import typing as t
from werkzeug.datastructures import ImmutableMultiDict

from src.db.models.films import Film
from flask_sqlalchemy import BaseQuery


def rating() -> BaseQuery:
    return Film.rating.desc()


def release_date() -> BaseQuery:
    return Film.release_date.desc()


orders = {
    'rating': rating,
    'release_date': release_date
}


def get_order(query: ImmutableMultiDict) -> t.Optional[BaseQuery]:
    for o_name, o_value in query.items():
        if o_value in orders:
            return orders[o_value]()
