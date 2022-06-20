import pytest

from src.domain.auth_dom import login
from src.exception.auth_exc import UserNotExistError, PasswordNotMatchError
from src.domain.schemes.user import StoredUserSchema, RegistrationUserSchema


def test_success(test_user: RegistrationUserSchema):
    user = login({'email': test_user.email, 'password1': test_user.password1})
    assert isinstance(user, StoredUserSchema)


@pytest.mark.parametrize('data', [
    (
            {
                'email': 'testtest@gmail.com',
                'password1': '1' * 8,
            }
    ),
    (
            {
                'email': 'testname@gmail.com',
                'password1': '1' * 15,
            }
    ),
    (
            {
                'email': 'testname123@gmail.com',
                'password1': '1' * 29,
            }
    ),
])
def test_user_not_exist_error(data: dict):
    with pytest.raises(UserNotExistError) as excinfo:
        login(data)
    assert excinfo.type is UserNotExistError


@pytest.mark.parametrize('password', ['1' * i for i in range(9, 30)])
def test_password_not_match_error(password: list, test_user):
    with pytest.raises(PasswordNotMatchError) as excinfo:
        login({'email': test_user.email, 'password1': password})
    assert excinfo.type is PasswordNotMatchError
