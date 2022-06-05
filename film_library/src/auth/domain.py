from flask import json

from models.schemes.user import RegistrationUserSchema, LoginUserSchema
from src.database import create_user, get_user
from src.utils import check_password
from src.auth import exception


def registration(data: json):
    user = RegistrationUserSchema(**data)
    create_user(user)


def login(data: json):
    user = LoginUserSchema(**data)
    stored_user = get_user(user)
    if not check_password(user.password1, stored_user.password1):
        raise exception.PasswordNotMatchError
    return stored_user
