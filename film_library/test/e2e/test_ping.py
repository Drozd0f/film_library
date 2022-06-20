from flask.testing import FlaskClient


def test_success(test_client: FlaskClient):
    response = test_client.get('/api/v1/films/ping')
    assert response.status_code == 200
    data = response.get_json()
    assert 'pong' == data['msg']
