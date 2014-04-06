import cherrypy
from cherrypy.lib.static import serve_file
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

# static_handler = cherrypy.tools.staticdir.handler(section="/", dir=os.path.join(current_dir, 'static'))
# cherrypy.tree.mount(static_handler, '/static')

def _serve(fname):
    return serve_file(os.path.join(current_dir, 'static', fname))

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        print("--")
        return _serve("foo.html")

class RR(object):


    @cherrypy.expose
    def index(self):
        return "The index of the root object"

config = {
    'global': {
        'environment': 'production',
        'log.screen': True,
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
        'engine.autoreload_on': True,
        'log.error_file': os.path.join(current_dir, 'errors.log'),
        'log.access_file': os.path.join(current_dir, 'access.log'),
    },
    '/':{
        'tools.staticdir.root' : current_dir,
    },
    '/static':{
        'tools.staticdir.on' : True,
        'tools.staticdir.dir' : 'static',
    },
}

if __name__ == '__main__':

    static_handler = cherrypy.tools.staticdir.handler(section="/", dir=os.path.join(current_dir, 'static'))
    cherrypy.tree.mount(static_handler, '/static')

    hw = HelloWorld()
    hw.rr = RR()
    cherrypy.tree.mount(hw, "/")

    cherrypy.engine.start()
    cherrypy.engine.block()
