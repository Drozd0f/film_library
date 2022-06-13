import typing as t

import pytest
from flask.testing import FlaskClient


@pytest.mark.parametrize('data', [
    (
            {
                'name': 'Test',
                'email': 'test@gmail.com',
                'password1': '1' * 8,
                'password2': '1' * 8
            }
    ),
    (
            {
                'name': 'TestName',
                'email': 'testname@gmail.com',
                'password1': '1' * 15,
                'password2': '1' * 15
            }
    ),
    (
            {
                'name': 'TestName123',
                'email': 'testname123@gmail.com',
                'password1': '1' * 29,
                'password2': '1' * 29
            }
    ),
])
def test_success(data: dict, test_client: FlaskClient):
    response = test_client.post('/api/v1/registration', json=data)
    assert response.status_code == 201
    data = response.get_json()
    assert 'user is created' == data['msg']


@pytest.mark.parametrize('data, expected_loc, expected_msg, expected_type', [
    (
        {'name': 'Test', 'email': 'test@gmail.com', 'password1': '1' * 2, 'password2': '1' * 2},
        ('password1', 'password2'),
        ('ensure this value has at least 8 characters', 'ensure this value has at least 8 characters'),
        ('value_error.any_str.min_length', 'value_error.any_str.min_length')
    ),
    (
        {'name': 'Te', 'email': 'test@gmail.com', 'password1': '1' * 8, 'password2': '1' * 8},
        ('name',),
        ('ensure this value has at least 3 characters',),
        ('value_error.any_str.min_length', )
    ),
    (
        {'name': 'Test', 'email': 'testgmail.com', 'password1': '1' * 8, 'password2': '1' * 8},
        ('email',),
        ('value is not a valid email address',),
        ('value_error.email',)
    ),
    (
        {'name': 'Test', 'email': 'test@gmail.com', 'password1': '1' * 9, 'password2': '1' * 8},
        (None,),
        ('passwords do not match',),
        ('value_error',)
    ),
    (
        {'email': 'test@gmail.com', 'password1': '1' * 8, 'password2': '1' * 8},
        ('name',),
        ('field required',),
        ('value_error.missing',)
    ),
    (
        {'name': 'Test', 'email': 'test@gmail.com', 'password1': '1' * 31, 'password2': '1' * 31},
        ('password1', 'password2'),
        ('ensure this value has at most 30 characters', 'ensure this value has at most 30 characters'),
        ('value_error.any_str.max_length', 'value_error.any_str.max_length')
    ),
    (
        {'name': 'Test' * 70, 'email': 'test@gmail.com', 'password1': '1' * 8, 'password2': '1' * 8},
        ('name',),
        ('ensure this value has at most 255 characters',),
        ('value_error.any_str.max_length',)
    ),
])
def test_validation_error(data: dict, expected_loc: t.Tuple[str], expected_msg: t.Tuple[str],
                          expected_type: t.Tuple[str], test_client: FlaskClient):
    response = test_client.post('/api/v1/registration', json=data)
    assert response.status_code == 400
    data = response.get_json()
    for idx, info in enumerate(data['msg']):
        if expected_loc[idx] is not None:
            assert expected_loc[idx] == info['loc'][0]
        assert expected_msg[idx] == info['msg']
        assert expected_type[idx] == info['type']


@pytest.mark.parametrize('data', [
    (
            {
                'name': 'Test',
                'email': 'test@gmail.com',
                'password1': '1' * 8,
                'password2': '1' * 8
            }
    ),
    (
            {
                'name': 'TestName',
                'email': 'testname@gmail.com',
                'password1': '1' * 15,
                'password2': '1' * 15
            }
    ),
    (
            {
                'name': 'TestName123',
                'email': 'testname123@gmail.com',
                'password1': '1' * 29,
                'password2': '1' * 29
            }
    ),
])
def test_user_exist(data: dict, test_client: FlaskClient):
    test_client.post('/api/v1/registration', json=data)
    response = test_client.post('/api/v1/registration', json=data)
    assert response.status_code == 409
    data = response.get_json()
    assert 'user with this email already exists' == data['msg']
