from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from web import config
from flask_login import LoginManager
from web.models import User
from flask_login import user_logged_in

web_app = Flask(__name__)
web_app.config.from_object(config)
web_db = SQLAlchemy(web_app)
web_app.secret_key = "not secret"
web_app.debug = True

login_manager = LoginManager()
login_manager.init_app(web_app)


def new_login(sender, **extra):
    print(sender)
    print(extra)
user_logged_in.connect(new_login, web_app)

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

import web.application
