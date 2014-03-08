from web import web_app
from api import api_app
from flask import Flask, redirect
from werkzeug.wsgi import DispatcherMiddleware

application = Flask(__name__)
application.wsgi_app = DispatcherMiddleware(web_app, {'/api': api_app})

# bad idea
# @web_app.errorhandler(404)
# def page_not_found(e):
#     return redirect("http://localhost:5000", code=301)

application.run(threaded=True)