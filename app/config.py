import os
from app.sockets import CoolSocket

STORAGE_PATH = os.environ.get("STORAGE_PATH", "/tmp")
SESSION_KEY = os.environ.get('SESSION_KEY', '8ffa7757-2452-49bd-a629-8d66dfeadd2f')

LOG_ERROR_FILE = os.environ.get('LOG_ERROR_FILE', "/tmp/errors.log")
LOG_ACCESS_FILE = os.environ.get('LOG_ACCESS_FILE', '/tmp/access.log')

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')

config = {
    'global': {
        'environment': 'production',
        'server.socket_host': '127.0.0.1',
        'engine.autoreload_on': True,
        # logs
        'log.screen': True,
        'log.error_file': LOG_ERROR_FILE,
        'log.access_file': LOG_ACCESS_FILE,
    },
    '/': {
        'tools.sessions.on': True,
        'tools.sessions.storage_type': "file",
        'tools.sessions.storage_path': STORAGE_PATH,
        'tools.sessions.timeout': 60,
        'tools.auth.on': True,
    },
}
ws_config = {
    '/': {
        'tools.websocket.on': True,
        'tools.websocket.handler_cls': CoolSocket,
    }
}

static_config = {
    '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': static_dir,
        'response.headers.connection': 'close'
    },
}
