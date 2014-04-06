import cherrypy
from functools import wraps
from app import config


cherrypy.config.update(config.config)


class allow(object):

    def __init__(self, methods=None):
        if not methods:
            methods = ['GET', 'HEAD']
        self.methods = methods

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            method = cherrypy.request.method.upper()
            if method not in self.methods:
                cherrypy.response.headers['Allow'] = ", ".join(self.methods)
                raise cherrypy.HTTPError(405)
            return f

        return wrapped_f