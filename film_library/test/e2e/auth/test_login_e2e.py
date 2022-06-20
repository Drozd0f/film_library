import random
import typing as t

import pytest
from flask.testing import FlaskClient
from flask_login import current_user

from src.domain.schemes.user import RegistrationUserSchema


def test_success(test_user: RegistrationUserSchema, test_client: FlaskClient):
    response = test_client.post(
        '/api/v1/login',
        json={
            'email': test_user.email,
            'password1': test_user.password1
        }
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'successful login' == data['msg']
    assert current_user.is_authenticated


@pytest.mark.parametrize('data, expected_loc, expected_msg, expected_type', [
    (
        {'email': 'test@gmail.com', 'password1': '1' * 2},
        ('password1',),
        ('ensure this value has at least 8 characters',),
        ('value_error.any_str.min_length',)
    ),
    (
        {'email': 'testgmail.com', 'password1': '1' * 8},
        ('email',),
        ('value is not a valid email address',),
        ('value_error.email',)
    ),
    (
        {'email': 'testgmail.com', 'password1': '1' * 2},
        ('email', 'password1'),
        ('value is not a valid email address', 'ensure this value has at least 8 characters'),
        ('value_error.email', 'value_error.any_str.min_length')
    ),
    (
        {'email': 'test@gmail.com', 'password1': '1' * 31},
        ('password1',),
        ('ensure this value has at most 30 characters',),
        ('value_error.any_str.max_length',)
    ),
    (
        {'email': 'testgmail.com', 'password1': '1' * 31},
        ('email', 'password1'),
        ('value is not a valid email address', 'ensure this value has at most 30 characters'),
        ('value_error.email', 'value_error.any_str.max_length')
    ),
])
def test_validation_error(data: dict, expected_loc: t.Tuple[str], expected_msg: t.Tuple[str],
                          expected_type: t.Tuple[str], test_client: FlaskClient):
    response = test_client.post('/api/v1/login', json=data)
    assert response.status_code == 400
    data = response.get_json()
    for idx, info in enumerate(data['msg']):
        if expected_loc[idx] is not None:
            assert info['loc'][0] == expected_loc[idx]
        assert info['msg'] == expected_msg[idx]
        assert info['type'] == expected_type[idx]


@pytest.mark.parametrize('data', [
    {
        'email': f'test{random.randrange(8, 29)}@gmail.com',
        'password1': '1' * random.randrange(8, 29)
    },
    {
        'email': f'test{random.randrange(8, 29)}@gmail.com',
        'password1': '1' * random.randrange(8, 29)
    },
    {
        'email': f'test{random.randrange(8, 29)}@gmail.com',
        'password1': '1' * random.randrange(8, 29)
    },
    {
        'email': f'test{random.randrange(8, 29)}@gmail.com',
        'password1': '1' * random.randrange(8, 29)
    },
    {
        'email': f'test{random.randrange(8, 29)}@gmail.com',
        'password1': '1' * random.randrange(8, 29)
    },
])
def test_user_not_exist(data: dict, test_client: FlaskClient):

    response = test_client.post('/api/v1/login', json=data)
    assert response.status_code == 404
    data = response.get_json()
    assert 'user don\'t exists' == data['msg']


@pytest.mark.parametrize('password', [
    '1' * rand_pass for rand_pass in range(9, 30)
])
def test_wrong_password(password: t.List[str], test_user: RegistrationUserSchema, test_client: FlaskClient):
    response = test_client.post(
        '/api/v1/login',
        json={
            'email': test_user.email,
            'password1': password
        }
    )
    assert response.status_code == 403
    data = response.get_json()
    assert 'wrong password' == data['msg']
