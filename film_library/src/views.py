from flask import json, Blueprint, Response


route_blueprint = Blueprint('route_blueprint', __name__)


@route_blueprint.route('/ping')
def ping():
    return Response(
        response=json.dumps({'msg': 'pong'}),
        status=200,
        mimetype='application/json'
    )
