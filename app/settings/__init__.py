import os
from os.path import dirname, abspath, join
from types import MappingProxyType

STORAGE_PATH = os.environ.get("STORAGE_PATH", "/tmp")
SESSION_KEY = os.environ.get('SESSION_KEY', '8ffa7757-2452-49bd-a629-8d66dfeadd2f')

LOG_ERROR_FILE = os.environ.get('LOG_ERROR_FILE', "/tmp/errors.log")
LOG_ACCESS_FILE = os.environ.get('LOG_ACCESS_FILE', '/tmp/access.log')

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)

REDIS_QUEUE_DB = os.environ.get("REDIS_QUEUE_DB", 0)

_current_dir = dirname(abspath(__file__))
current_dir = abspath(join(_current_dir, os.pardir))
static_dir = abspath(join(current_dir, 'static'))

REDIS_QUEUE_KWARGS = MappingProxyType({
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "db": REDIS_QUEUE_DB, })