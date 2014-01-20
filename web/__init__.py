from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from web import config

web_app = Flask(__name__)
web_app.config.from_object(config)
web_db = SQLAlchemy(web_app)

import web.application
