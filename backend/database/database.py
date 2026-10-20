"""SQLite connections belong to the thread and service call creating them."""

from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
import sqlite3
from backend.path_resolver import PathResolver

_connections = ContextVar("launcher_connections", default=None)


@contextmanager
def database_scope():
    if _connections.get() is not None:
        yield
        return
    opened = []
    token = _connections.set(opened)
    try:
        yield
    finally:
        for db in reversed(opened):
            db.close()
        _connections.reset(token)


def scoped(method):
    @wraps(method)
    def call(*args, **kwargs):
        with database_scope():
            return method(*args, **kwargs)

    return call


class Database:
    def __init__(self):
        self.db_path = PathResolver.data() / "library.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.db_path, timeout=30)
        self.connection.row_factory = sqlite3.Row
        self._closed = False
        opened = _connections.get()
        if opened is not None:
            opened.append(self)

    def cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        if not self._closed:
            self.connection.close()
            self._closed = True
