from app.sockets import CoolSocket
from app import settings

config = {
    'global': {
        'environment': 'production',
        'server.socket_host': '127.0.0.1',
        'engine.autoreload_on': True,
        # logs
        'log.screen': True,
        'log.error_file': settings.LOG_ERROR_FILE,
        'log.access_file': settings.LOG_ACCESS_FILE,
    },
    '/': {
        'tools.sessions.on': True,
        'tools.sessions.storage_type': "file",
        'tools.sessions.storage_path': settings.STORAGE_PATH,
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
        'tools.staticdir.dir': settings.static_dir,
        'response.headers.connection': 'close'
    },
}
