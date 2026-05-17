import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_article_connection() -> sqlite3.Connection:
    try:
        path = os.path.normpath(os.path.join(BASE_DIR, '..', 'blog.db'))
        return sqlite3.connect(path)
    except sqlite3.OperationalError:
        raise ConnectionError("Error while connecting to article database")

def get_user_connection() -> sqlite3.Connection:
    try:
        path = os.path.normpath(os.path.join(BASE_DIR, '..', 'user.db'))
        return sqlite3.connect(path)
    except sqlite3.OperationalError:
        raise ConnectionError("Error while connecting to user database")