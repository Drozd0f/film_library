from flask import json, Blueprint, Response, request
from pydantic import ValidationError

from models.schemes.film import FilmModelSchema

route_blueprint = Blueprint('route_blueprint', __name__)


@route_blueprint.route('/ping')
def ping():
    return Response(
        response=json.dumps({'msg': 'pong'}),
        status=200,
        mimetype='application/json'
    )


@route_blueprint.route('/film', methods=['POST'])
def create_film():
    try:
        film = FilmModelSchema(**request.get_json())  # noqa: F841 (variable use in domain)
    except ValidationError as e:
        return Response(
            response=json.dumps({'validation_error': e.errors()}),
            status=400,
            mimetype='application/json'
        )
    # TODO: domain function
    return Response(
        response=json.dumps({'msg': 'film is created'}),
        status=200,
        mimetype='application/json'
    )
