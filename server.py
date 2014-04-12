from app import settings
from app.settings import config
import os
from app import root, socket_root
import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool

if __name__ == "__main__":
    kwargs = {
        'section': '/',
        'dir': os.path.join(settings.current_dir, 'static')
    }
    static_handler = cherrypy.tools.staticdir.handler(**kwargs)
    cherrypy.tree.mount(static_handler, '/static')

    cherrypy.tree.mount(root)
    cherrypy.tree.mount(None, '/static', config=config.static_config)
    cherrypy.tree.mount(socket_root, "/ws", config=config.ws_config)

    WebSocketPlugin(cherrypy.engine).subscribe()

    cherrypy.tools.websocket = WebSocketTool()
    cherrypy.tree.mount(root, "/")

    cherrypy.server.unsubscribe()
    server = cherrypy._cpserver.Server()

    server.socket_host = "127.0.0.1"
    server.socket_port = 8080
    server.thread_pool = 30
    server.subscribe()

    server2 = cherrypy._cpserver.Server()
    server2.socket_host = "127.0.0.1"
    server2.socket_port = 8081
    server2.thread_pool = 30
    server2.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()


