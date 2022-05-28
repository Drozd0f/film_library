from flask import json

from src import app


@app.route('/ping/')
def ping():
    return app.response_class(
        response=json.dumps({'msg': 'pong'}),
        status=200,
        mimetype='application/json'
    )
