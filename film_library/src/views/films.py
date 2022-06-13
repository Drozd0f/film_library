from flask import json, Blueprint, Response, request
from flask_login import login_required
from pydantic import ValidationError

from src.domain import films_dom
from src.exception import films_exc


film_blueprint = Blueprint('film_blueprint', __name__, url_prefix='/api/v1')


@film_blueprint.route('/films/ping')
def ping():
    return Response(
        response=json.dumps({'msg': 'pong'}),
        status=200,
        mimetype='application/json'
    )


@film_blueprint.route('/films/<int:film_id>', methods=['GET'])
def get_film_by_id(film_id: int):
    try:
        film = films_dom.get_film_by_id(film_id)
    except films_exc.FilmIdNotFoundError:
        return Response(
            response=json.dumps({'msg': 'film don\'t exists'}),
            status=404,
            mimetype='application/json'
        )
    return Response(
        response=json.dumps(film.dict(), sort_keys=True, default=str),
        status=200,
        mimetype='application/json'
    )


@film_blueprint.route('/films', methods=['POST'])
@login_required
def create_film():
    try:
        film = films_dom.create_film(request.get_json())
    except ValidationError as e:
        return Response(
            response=json.dumps({'msg': e.errors()}),
            status=400,
            mimetype='application/json'
        )
    except films_exc.FilmNameExist:
        return Response(
            response=json.dumps({'msg': 'film with this name already exists'}),
            status=409,
            mimetype='application/json'
        )  # TODO: is director exists
    except films_exc.GenresNotMatchError:
        return Response(
            response=json.dumps({'msg': 'unknown genres ids'}),
            status=400,
            mimetype='application/json'
        )
    return Response(
        response=json.dumps(film.dict(), sort_keys=True, default=str),
        status=201,
        mimetype='application/json'
    )


@film_blueprint.route('/films/<int:film_id>', methods=['PATCH'])
@login_required
def update_films(film_id: int):
    try:
        film = films_dom.update_film(film_id, request.get_json())
    except ValidationError as e:
        return Response(
            response=json.dumps({'msg': e.errors()}),
            status=400,
            mimetype='application/json'
        )
    except films_exc.FilmNameExist:
        return Response(
            response=json.dumps({'msg': 'film with this name already exists'}),
            status=409,
            mimetype='application/json'
        )  # TODO: is director exists
    except films_exc.FilmIdNotFoundError:
        return Response(
            response=json.dumps({'msg': 'film don\'t exists'}),
            status=404,
            mimetype='application/json'
        )
    except films_exc.UserNotOwnerError:
        return Response(
            response=json.dumps({'msg': 'permission denied'}),
            status=403,
            mimetype='application/json'
        )
    except films_exc.GenresNotMatchError:
        return Response(
            response=json.dumps({'msg': 'unknown genres ids'}),
            status=400,
            mimetype='application/json'
        )
    return Response(
        response=json.dumps(film.dict(), sort_keys=True, default=str),
        status=200,
        mimetype='application/json'
    )


@film_blueprint.route('/films/<int:film_id>', methods=['DELETE'])
@login_required
def delete_films(film_id: int):
    try:
        film = films_dom.delete_film(film_id)
    except films_exc.FilmIdNotFoundError:
        return Response(
            response=json.dumps({'msg': 'film don\'t exists'}),
            status=404,
            mimetype='application/json'
        )
    except films_exc.UserNotOwnerError:
        return Response(
            response=json.dumps({'msg': 'permission denied'}),
            status=403,
            mimetype='application/json'
        )
    return Response(
        response=json.dumps(film.dict(), sort_keys=True, default=str),
        status=200,
        mimetype='application/json'
    )


@film_blueprint.route('/films', methods=['GET'])
def get_films():
    return Response(
        response=json.dumps(films_dom.get_films(request.args), sort_keys=True, default=str),
        status=200,
        mimetype='application/json'
    )
