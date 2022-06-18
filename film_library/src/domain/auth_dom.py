from werkzeug.security import generate_password_hash

from flask import json

from src.db.database import create_user, get_user
from src.domain.schemes import user
from src.exception import auth_exc
from src.utils import check_password


def registration(data: json):
    new_user = user.RegistrationUserSchema(**data)
    if get_user(new_user.email) is not None:
        raise auth_exc.UserExistError
    new_user.password1 = generate_password_hash(new_user.password1, method='sha256')
    new_user.password2 = generate_password_hash(new_user.password2, method='sha256')
    create_user(new_user)


def login(data: json) -> user.StoredUserSchema:
    login_user = user.LoginUserSchema(**data)
    stored_user = get_user(login_user.email)
    if stored_user is None:
        raise auth_exc.UserNotExistError
    if not check_password(login_user.password1, stored_user.password1):
        raise auth_exc.PasswordNotMatchError
    return user.StoredUserSchema.from_orm(stored_user)
