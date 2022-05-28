import os


class BaseConfig:
    # TODO SQLALCHEMY_TRACK_MODIFICATIONS = False
    pass


class TestingConfig(BaseConfig):
    DEBUG = True
    # TODO SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB_URI')
