import typing as t
from werkzeug.datastructures import ImmutableMultiDict

from flask_sqlalchemy import BaseQuery

from models.films import Film
from models.genres import Genre


def genre(genres_ids: t.List[int]) -> BaseQuery:
    return Genre.genre_id.in_(genres_ids)


def release_year(release_year_range: list) -> BaseQuery:
    return Film.release_date.between(*release_year_range)


def directors(directors_id: t.List[int]) -> BaseQuery:
    return Film.director_id.in_(directors_id)


def name(name_film: t.List[str]) -> BaseQuery:
    return Film.name.ilike(f'%{name_film[0]}%')


filters = {
    'genres': genre,
    'release_year_range': release_year,
    'directors': directors,
    'name': name
}


def filter_generator(query: ImmutableMultiDict):
    for f_name, f_value in query.items():
        if f_name in filters:
            yield filters[f_name](query.getlist(f_name))
