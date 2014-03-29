from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session
from web import config
from flask_login import LoginManager
from web.models import User
from flask_login import user_logged_in, user_logged_out, current_user, session_protected

web_app = Flask(__name__)
web_app.config.from_object(config)



web_db = SQLAlchemy(web_app)
web_app.secret_key = "not secret"
web_app.debug = True

login_manager = LoginManager()
login_manager.init_app(web_app)


def new_login(sender, **extra):
    print("login", sender, str(extra))
    print(current_user)
    print(session)
    session.permanent = True
    web_app.permanent_session_lifetime = timedelta(minutes=1)


def new_logout(sender, **extra):
    print("logout", str(sender), str(extra))


def new_logout(sender, **extra):
    print("logout", str(sender), str(extra))


def new_expired_session(sender, **extra):
    print("session", str(sender), str(extra))


session_protected.connect(new_expired_session, web_app)
user_logged_in.connect(new_login, web_app)
user_logged_out.connect(new_logout, web_app)


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


import web.application
