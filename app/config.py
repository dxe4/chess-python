import os
from app.sockets import CoolSocket

SESSION_KEY = '8ffa7757-2452-49bd-a629-8d66dfeadd2f'
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')
config = {
    'global': {
        'environment': 'production',
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
        'engine.autoreload_on': True,
        # logs
        'log.screen': True,
        'log.error_file': '/tmp/errors.log',
        'log.access_file': '/tmp/access.log',
    },
    '/': {
        'tools.sessions.on': True,
        'tools.sessions.storage_type': "file",
        'tools.sessions.storage_path': "/tmp",
        'tools.sessions.timeout': 60,
        'tools.auth.on': True,
    },
    '/ws': {
        'tools.websocket.on': True,
        'tools.websocket.handler_cls': CoolSocket
    },
    # 'server.socket_port': 9000,
}