import typing as t
from werkzeug.security import check_password_hash


def check_password(login_password: str, stored_password: str) -> bool:
    return check_password_hash(stored_password, login_password)


def unique_list(not_unique_list: list) -> t.List[int]:
    return list(set(not_unique_list))
