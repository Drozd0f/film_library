from flask import json

from models.users import User
from models.schemes.user import RegistrationUserSchema, LoginUserSchema
from src.database import create_user
from src.utils import check_password
from src.auth import exception


def registration(data: json):
    user = RegistrationUserSchema(**data)
    if User.get_by_email(user.email) is not None:
        raise exception.UserExistError
    create_user(user)


def login(data: json):
    user = LoginUserSchema(**data)
    stored_user = User.get_by_email(user.email)
    if stored_user is None:
        raise exception.UserNotExistError
    if not check_password(user.password1, stored_user.password1):
        raise exception.PasswordNotMatchError
    return stored_user
