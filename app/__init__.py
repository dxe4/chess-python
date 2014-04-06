import cherrypy
from app import config
cherrypy.config.update(config.config)
