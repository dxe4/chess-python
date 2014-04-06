import os
from cherrypy.lib.static import serve_file
import cherrypy
from app import config


def _serve(*args):
    print(os.path.join(config.current_dir, 'static', *args))
    return serve_file(os.path.join(config.current_dir, 'static', *args))


class Home(object):
    @cherrypy.expose
    def index(self):
        return _serve("templates", "index.html")


if __name__ == '__main__':
    kwargs = {
        'section': '/',
        'dir': os.path.join(config.current_dir, 'static')
    }
    static_handler = cherrypy.tools.staticdir.handler(**kwargs)
    cherrypy.tree.mount(static_handler, '/static')

    hw = Home()
    cherrypy.tree.mount(hw)

    cherrypy.engine.start()
    cherrypy.engine.block()
