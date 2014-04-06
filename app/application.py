import os
from cherrypy.lib.static import serve_file
from cherrypy import expose
import cherrypy
from app import config, allow
from app.auth import require


def _serve(*args):
    return serve_file(os.path.join(config.current_dir, 'static', *args))


class Root(object):
    @allow(methods=["GET", "HEAD"])
    @expose
    def index(self):
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
    def login(self):
        pass


    @allow(methods=["POST"])
    @expose
    @require()
    def logout(self):
        pass

    @expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def my_route(self):

        result = {"operation": "request", "result": "success"}

        input_json = cherrypy.request.json
        value = input_json["my_key"]
        return result


if __name__ == '__main__':
    kwargs = {
        'section': '/',
        'dir': os.path.join(config.current_dir, 'static')
    }
    static_handler = cherrypy.tools.staticdir.handler(**kwargs)
    cherrypy.tree.mount(static_handler, '/static')

    root = Root()
    root.api = Api()

    cherrypy.tree.mount(root)
    cherrypy.tree.mount(None, '/static', config={
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': config.static_dir,
            'response.headers.connection': 'close'
        },
    })
    cherrypy.engine.start()
    cherrypy.engine.block()
