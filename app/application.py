from app.settings import config
import os
from cherrypy.lib.static import serve_file
from cherrypy import expose
import cherrypy
from app import allow
from app.auth import require


def _serve(*args):
    return serve_file(os.path.join(config.current_dir, 'static', *args))


class Root(object):
    @allow(methods=["GET", "HEAD"])
    @expose
    def index(self):
        print(cherrypy.request.cookie)
        return _serve("templates", "index.html")


class Api(object):
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }

    @allow(methods=["GET"])
    @expose
    @require()
    def join_queue(self):
        pass


    @allow(methods=["POST"])
    @expose
    @cherrypy.tools.json_in()
    def login(self):
        input_json = cherrypy.request.json
        username = input_json["username"]
        cherrypy.session[config.SESSION_KEY] = cherrypy.request.login = username
        cherrypy.response.cookie["username"] = username
        cherrypy.response.cookie["username"]["path"] = "/"
        return username


    @allow(methods=["POST"])
    @expose
    @require()
    def logout(self):
        sess = cherrypy.session
        username = sess.get(config.SESSION_KEY, None)
        sess[config.SESSION_KEY] = None
        if username:
            cherrypy.request.login = None

    @expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def my_route(self):
        result = {"operation": "request", "result": "success"}

        input_json = cherrypy.request.json
        value = input_json["my_key"]
        return result


class SocketRoot(object):
    @cherrypy.expose
    @require()
    def index(self):
        cool_socket = cherrypy.request.ws_handler
        print(cherrypy.request.cookie)


root = Root()
root.api = Api()
socket_root = SocketRoot()