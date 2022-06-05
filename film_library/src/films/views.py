from flask import json, Blueprint, Response, request
from pydantic import ValidationError

from src.films import domain
from models.schemes.film import RequestFilmSchema


film_blueprint = Blueprint('film_blueprint', __name__)


@film_blueprint.route('/ping')
def ping():
    return Response(
        response=json.dumps({'msg': 'pong'}),
        status=200,
        mimetype='application/json'
    )


@film_blueprint.route('/api/v1/films', methods=['POST'])
def create_film():
    try:
        film = RequestFilmSchema(**request.get_json())  # noqa: F841 (variable use in domain)
    except ValidationError as e:
        return Response(
            response=json.dumps({'msg': e.errors()}),
            status=400,
            mimetype='application/json'
        )
    # TODO: domain function
    return Response(
        response=json.dumps({'msg': 'film is created'}),
        status=200,
        mimetype='application/json'
    )


@film_blueprint.route('/api/v1/films', methods=['GET'])
def get_films():
    return Response(
        response=json.dumps(domain.get_films(request.args), sort_keys=True, default=str),
        status=200,
        mimetype='application/json'
    )
