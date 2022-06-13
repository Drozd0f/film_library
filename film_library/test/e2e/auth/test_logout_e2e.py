from flask.testing import FlaskClient
from flask_login import current_user

from src.domain.schemes.user import RegistrationUserSchema


def test_success(test_user: RegistrationUserSchema, test_client: FlaskClient):
    test_client.post(
        '/api/v1/login',
        json={
            'email': test_user.email,
            'password1': test_user.password1
        }
    )
    response = test_client.get('/api/v1/logout')
    assert response.status_code == 200
    data = response.get_json()
    assert 'successful logout' == data['msg']
    assert current_user.is_anonymous


def test_unauthorized(test_client: FlaskClient):
    response = test_client.get('/api/v1/logout')
    assert response.status_code == 401
    data = response.get_json()
    assert data['msg'] == 'user unauthorized'
