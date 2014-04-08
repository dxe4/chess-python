import os
import cherrypy
from app import config
from app import root, socket_root
import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from app.sockets import CoolSocket

if __name__ == "__main__":
    pass

    kwargs = {
        'section': '/',
        'dir': os.path.join(config.current_dir, 'static')
    }
    static_handler = cherrypy.tools.staticdir.handler(**kwargs)
    cherrypy.tree.mount(static_handler, '/static')

    cherrypy.tree.mount(root)
    cherrypy.tree.mount(None, '/static', config={
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': config.static_dir,
            'response.headers.connection': 'close'
        },
    })

    # cherrypy.config.update({'server.socket_port': 9000})
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

    server3 = cherrypy._cpserver.Server()
    ws_config = {'/': {'tools.websocket.on': True,
                       'tools.websocket.handler_cls': CoolSocket,
                       # 'server.socket_port': 9000,

    }}
    cherrypy.tree.mount(socket_root, "/ws", config=ws_config)
    server3.socket_host = "127.0.0.1"
    server3.socket_port = 9000
    server3.thread_pool = 30

    server3.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()


