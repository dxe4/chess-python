from web import web_app
from api import api_app
from flask import Flask, redirect, session, request, after_this_request, g
from werkzeug.wsgi import DispatcherMiddleware
from web.sessions import RedisSessionInterface

session_interface = RedisSessionInterface()
web_app.session_interface = session_interface
api_app.session_interface = session_interface

application = Flask(__name__)
application.wsgi_app = DispatcherMiddleware(web_app, {'/api': api_app})

# bad idea
# @web_app.errorhandler(404)
# def page_not_found(e):
#     return redirect("http://localhost:5000", code=301)



@web_app.before_request
def renew_username_cookie():
    username = session.get("username", "")
    @after_this_request
    def _renew_username_cookie(response):
        response.set_cookie("username",username)
        return response
    g.username = username

application.run(threaded=True)