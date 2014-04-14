import os
import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from app import settings
from app.settings import config
from app import root, socket_root
from workers.queue import start_match_process


def make_servers(ports: list, pool_size:int):
    def _make(port: int):
        server = cherrypy._cpserver.Server()
        server.socket_host = "127.0.0.1"
        server.socket_port = port
        server.thread_pool = pool_size
        server.subscribe()
        return server

    return [_make(i) for i in ports]


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
    servers = make_servers([8080, 8081], 10)

    start_match_process()

    cherrypy.engine.start()
    cherrypy.engine.block()


