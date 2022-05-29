from flask import Flask

from config import TestingConfig
from src.database import init_db

app = Flask(__name__)
app.config.from_object(TestingConfig)

from . import views

init_db()
