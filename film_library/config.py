import os
from dataclasses import dataclass

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker


class BaseConfig:
    pass


class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB_URI')


@dataclass
class DataBaseConfig:
    Base = declarative_base()
    engine = create_engine(os.environ.get('TEST_DB_URI'))
    db_session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
    )
