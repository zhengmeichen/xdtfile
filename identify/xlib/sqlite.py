import sqlite3
import threading

import sys

DICTROW = True
AUTOCOMMIT = True
local = threading.local()
PY3K = sys.version_info >= (3, 0, 0)
TEXT_FACTORY = str if PY3K else unicode
DBFILE = 'conf.sqlite'
INTERFACE = 'SQLITE'


class DictRow(dict):
    @staticmethod
    def __new__(cls, b1, c1):
        return dict({b[0]: c for b, c in zip(b1.description, c1)})


class database:
    def __init__(self, dict=DICTROW):
        if hasattr(local, 'sqlite3'):
            self.db = local.sqlite3
        else:
            self.db = local.sqlite3 = sqlite3.connect(DBFILE)
            self.db.text_factory = TEXT_FACTORY
            self.db.execute('pragma foreign_keys = on')

        if dict:
            self.db.row_factory = DictRow
        else:
            self.db.row_factory = None  # sqlite3.Row

    def __enter__(self):
        return self.db.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_type, sqlite3.IntegrityError):
            self.db.rollback()
        if AUTOCOMMIT:
            self.db.commit()
