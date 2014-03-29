from collections import deque
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from web import config

api_app = Flask(__name__)
api_app.config.from_object(config)
api_db = SQLAlchemy(api_app)

api_app.secret_key = "not secret"

# from redis import Redis
# redis = Redis(host='localhost', port=6379, db=0)
start_queue = deque()
pending = {}
games = {}

from api import application
