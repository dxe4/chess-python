import os

current_dir = os.path.dirname(os.path.abspath(__file__))
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
        # 'log.error_file': os.path.join(current_dir, 'errors.log'),
        # 'log.access_file': os.path.join(current_dir, 'access.log'),
    },
    '/': {
        'tools.staticdir.root': current_dir,
        # sessions
        'tools.sessions.on': True,
        # 'tools.sessions.storage_type': "file",
        # 'tools.sessions.storage_path': "/tmp",
        'tools.sessions.timeout': 60,
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static',
    },
}