import typing as t

from models.films import Film
from models.schemes.film import ResponseFilmSchema
from models.schemes.paginator import Paginator
from src import database


def convert_orm_to_pydent_dict(orm_models: t.List[Film]) -> t.List[dict]:
    return [ResponseFilmSchema.from_orm(orm_model).dict() for orm_model in orm_models]


def get_films(query: dict) -> dict:
    paginator = Paginator(
        query.get('page', '1'),
        query.get('limit', '10')
    )
    films, count_films = database.get_films(query, paginator.page, paginator.limit)
    paginator.total_pages = count_films
    return {
        'films': convert_orm_to_pydent_dict(films),
        'paginator': paginator.to_dict()
    }
