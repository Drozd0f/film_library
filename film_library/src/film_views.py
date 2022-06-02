from flask import json, Blueprint, Response, request
from pydantic import ValidationError

from models.schemes.film import FilmModelSchema


film_blueprint = Blueprint('film_blueprint', __name__)


@film_blueprint.route('/ping')
def ping():
    return Response(
        response=json.dumps({'msg': 'pong'}),
        status=200,
        mimetype='application/json'
    )


@film_blueprint.route('/api/v1/film', methods=['POST'])
def create_film():
    try:
        film = FilmModelSchema(**request.get_json())  # noqa: F841 (variable use in domain)
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
