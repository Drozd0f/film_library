from flask import json, Blueprint, Response, request
from flask_login import login_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError, NoResultFound
from pydantic import ValidationError

from models.schemes.user import UserModelSchema
from src.database import create_user, get_user
from src.utils import check_password


auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route('/api/v1/registration', methods=['POST'])
def registration():
    try:
        user = UserModelSchema(**request.get_json())
        create_user(user)
    except ValidationError as e:
        return Response(
            response=json.dumps({'msg': e.errors()}),
            status=400,
            mimetype='application/json'
        )
    except IntegrityError:
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


@auth_blueprint.route('/api/v1/login', methods=['POST'])
def login():
    data = request.get_json()
    remember = bool(data.pop('remember', None))
    try:
        user = UserModelSchema(**request.get_json())
        stored_user = get_user(user)
    except ValidationError as e:
        return Response(
            response=json.dumps({'msg': e.errors()}),
            status=400,
            mimetype='application/json'
        )
    except NoResultFound:
        return Response(
            response=json.dumps({'msg': 'user don\'t exists'}),
            status=404,
            mimetype='application/json'
        )
    if not check_password(user.password1, stored_user.password1):
        return Response(
            response=json.dumps({'msg': 'wrong password'}),
            status=400,
            mimetype='application/json'
        )
    login_user(stored_user, remember=remember)
    return Response(
        response=json.dumps({'msg': 'successful login'}),
        status=200,
        mimetype='application/json'
    )


@auth_blueprint.route('/api/v1/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return Response(
        response=json.dumps({'msg': 'successful logout'}),
        status=200,
        mimetype='application/json'
    )
