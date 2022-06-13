from werkzeug.security import check_password_hash

import pytest

from src.domain.auth_dom import registration
from src.exception.auth_exc import UserExistError
from src.db.models.users import User


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
def test_success(data: dict):
    registration(data)
    user = User.get_by_email(data['email'])
    assert data['name'] == user.name
    assert data['email'] == user.email
    assert check_password_hash(user.password1, data['password1'])
    assert check_password_hash(user.password2, data['password2'])


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
def test_user_exist_error(data: dict):
    registration(data)
    with pytest.raises(UserExistError) as excinfo:
        registration(data)
    assert excinfo.type is UserExistError
