from src import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    is_staff = db.Column(db.Boolean, default=False)

    def __init__(self, name: str, surname: str, is_staff: bool = False):
        self.name = name
        self.surname = surname
        self.is_staff = is_staff

    def __repr__(self):
        return f'<User(user_id={self.user_id}, name={self.name}, ' \
               f'surname={self.surname}, is_staff={self.is_staff})>'
