from pydantic import BaseModel, root_validator, constr, EmailStr

from flask_login import UserMixin


class BaseUserSchema(BaseModel):
    email: EmailStr
    password1: constr(min_length=8, max_length=30)


class RegistrationUserSchema(BaseUserSchema):
    name: constr(min_length=3, max_length=255)
    password2: constr(min_length=8, max_length=30)

    @root_validator
    def passwords_match(cls, values):
        pw1, pw2 = values.get('password1'), values.get('password2')
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return values


class LoginUserSchema(BaseUserSchema):
    pass


class StoredUserSchema(BaseModel, UserMixin):
    user_id: int
    name: constr(min_length=3, max_length=255)
    is_staff: bool

    def get_id(self):
        return self.user_id

    class Config:
        orm_mode = True
