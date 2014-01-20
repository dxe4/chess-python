from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from web import config

api_app = Flask(__name__)
api_app.config.from_object(config)
api_db = SQLAlchemy(api_app)

from api import application
