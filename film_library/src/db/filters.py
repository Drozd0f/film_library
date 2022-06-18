import typing as t
from werkzeug.datastructures import ImmutableMultiDict

from flask_sqlalchemy import BaseQuery
from sqlalchemy.sql.elements import BinaryExpression

from src.db.models.films import Film
from src.db.models.genres import Genre


def genre(genres_ids: t.List[str]) -> BinaryExpression:
    return Genre.genre_id.in_(genres_ids)


def release_year(release_year_range: list) -> BinaryExpression:
    return Film.release_date.between(*release_year_range)


def directors(directors_id: t.List[str]) -> BinaryExpression:
    return Film.director_id.in_(directors_id)


def name(name_film: t.List[str]) -> BinaryExpression:
    return Film.name.ilike(f'%{name_film[0]}%')


filters = {
    'genres': genre,
    'release_year_range': release_year,
    'directors': directors,
    'name': name
}


def filter_generator(query: ImmutableMultiDict) -> BinaryExpression:
    for f_name, f_value in query.items():
        if f_name in filters:
            yield filters[f_name](query.getlist(f_name))


def with_filter(base_query: BaseQuery, query_params: ImmutableMultiDict) -> BaseQuery:
    get_filters = list(filter_generator(query_params))
    if query_params.get('genres'):
        base_query = base_query.join(Film.genres)
    return base_query.filter(*get_filters)
