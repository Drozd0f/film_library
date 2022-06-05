from flask import json, Blueprint, Response, request
from flask_login import login_required, current_user
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from src.films import domain
from src.films import exception


film_blueprint = Blueprint('film_blueprint', __name__)


@film_blueprint.route('/ping')
def ping():
    return Response(
        response=json.dumps({'msg': 'pong'}),
        status=200,
        mimetype='application/json'
    )


@film_blueprint.route('/api/v1/films', methods=['POST'])
@login_required
def create_film():
    try:
        domain.create_film(current_user, request.get_json())
    except ValidationError as e:
        return Response(
            response=json.dumps({'msg': e.errors()}),
            status=400,
            mimetype='application/json'
        )
    except IntegrityError:
        return Response(
            response=json.dumps({'msg': 'film with this name already exists'}),
            status=409,
            mimetype='application/json'
        )  # TODO: is director exists
    except exception.GenresNotMatchError:
        return Response(
            response=json.dumps({'msg': 'unknown genres ids'}),
            status=400,
            mimetype='application/json'
        )
    return Response(
        response=json.dumps({'msg': 'film is created'}),
        status=200,
        mimetype='application/json'
    )


@film_blueprint.route('/api/v1/films', methods=['PATCH'])
@login_required
def update_films():
    try:
        domain.update_film(current_user, request.get_json())
    except ValidationError as e:
        return Response(
            response=json.dumps({'msg': e.errors()}),
            status=400,
            mimetype='application/json'
        )
    except IntegrityError:
        return Response(
            response=json.dumps({'msg': 'film with this name already exists'}),
            status=409,
            mimetype='application/json'
        )  # TODO: is director exists
    except exception.FilmIdNotFoundError:
        return Response(
            response=json.dumps({'msg': 'film don\'t exists'}),
            status=404,
            mimetype='application/json'
        )
    except exception.UserNotOwnerError:
        return Response(
            response=json.dumps({'msg': 'user has insufficient rights'}),
            status=403,
            mimetype='application/json'
        )
    except exception.GenresNotMatchError:
        return Response(
            response=json.dumps({'msg': 'unknown genres ids'}),
            status=400,
            mimetype='application/json'
        )
    return Response(
        response=json.dumps({'msg': 'film is updated'}),
        status=200,
        mimetype='application/json'
    )


@film_blueprint.route('/api/v1/films', methods=['DELETE'])
@login_required
def delete_films():
    try:
        domain.delete_film(current_user, request.get_json())
    except ValidationError as e:
        return Response(
            response=json.dumps({'msg': e.errors()}),
            status=400,
            mimetype='application/json'
        )
    except exception.FilmIdNotFoundError:
        return Response(
            response=json.dumps({'msg': 'film don\'t exists'}),
            status=404,
            mimetype='application/json'
        )
    except exception.UserNotOwnerError:
        return Response(
            response=json.dumps({'msg': 'user has insufficient rights'}),
            status=403,
            mimetype='application/json'
        )
    except exception.GenresNotMatchError:
        return Response(
            response=json.dumps({'msg': 'unknown genres ids'}),
            status=400,
            mimetype='application/json'
        )
    return Response(
        response=json.dumps({'msg': 'film is deleted'}),
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
