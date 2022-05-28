from flask import Flask

from config import TestingConfig

app = Flask(__name__)
app.config.from_object(TestingConfig)

from . import views
