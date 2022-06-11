from flask import json, Blueprint, Response, request
from flask_login import login_user, login_required, logout_user
from pydantic import ValidationError

from src.auth import domain, exception

auth_blueprint = Blueprint('auth_blueprint', __name__, url_prefix='/api/v1')


@auth_blueprint.route('/registration', methods=['POST'])
def registration():
    try:
        domain.registration(request.get_json())
    except ValidationError as e:
        return Response(
            response=json.dumps({'msg': e.errors()}),
            status=400,
            mimetype='application/json'
        )
    except exception.UserExistError:
        return Response(
            response=json.dumps({'msg': 'user with this email already exists'}),
            status=409,
            mimetype='application/json'
        )
    return Response(
        response=json.dumps({'msg': 'user is created'}),
        status=201,
        mimetype='application/json'
    )


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    remember = bool(data.pop('remember', None))
    try:
        user = domain.login(request.get_json())
    except ValidationError as e:
        return Response(
            response=json.dumps({'msg': e.errors()}),
            status=400,
            mimetype='application/json'
        )
    except exception.UserNotExistError:
        return Response(
            response=json.dumps({'msg': 'user don\'t exists'}),
            status=404,
            mimetype='application/json'
        )
    except exception.PasswordNotMatchError:
        return Response(
            response=json.dumps({'msg': 'wrong password'}),
            status=400,
            mimetype='application/json'
        )
    login_user(user, remember=remember)
    return Response(
        response=json.dumps({'msg': 'successful login'}),
        status=200,
        mimetype='application/json'
    )


@auth_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return Response(
        response=json.dumps({'msg': 'successful logout'}),
        status=200,
        mimetype='application/json'
    )
