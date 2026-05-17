import os
import sqlite3

from pwdlib import PasswordHash

from database.connection import get_user_connection
from utils.exceptions import UserExistsError, LoginFailedError
from utils.models import UserRegister, UserLogin, User

def init_user_db() -> None:
    with get_user_connection() as conn:
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS user (
                                                         id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                         username TEXT UNIQUE NOT NULL,
                                                         email TEXT UNIQUE NOT NULL,
                                                         password TEXT NOT NULL
                     )
                     """)

def register_user_db(user: UserRegister) -> None:
    try:
        with get_user_connection() as conn:
            password_hash = PasswordHash.recommended()
            hashed_password = password_hash.hash(user.password)
            conn.execute("""
                         INSERT INTO user (username, email, password) VALUES (?, ?, ?)
                         """,
                         (user.username, user.email, hashed_password)
                         )
    except sqlite3.IntegrityError:
        raise UserExistsError("Error while creating user")

def login_user_db(login: UserLogin) -> User:
    try:
        with get_user_connection() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("""
                               SELECT id, username, password FROM user WHERE username = ?
                               """,
                               (login.username,)
                               ).fetchone()
            return User(**row)
    except sqlite3.IntegrityError:
        raise LoginFailedError("Error while login user")

def get_user_by_id(id: int) -> str:
    try:
        with get_user_connection() as conn:
            row = conn.execute("""
                               SELECT username FROM user WHERE id = ?
                               """,
                               (id,)
                               ).fetchone()
            return row
    except sqlite3.IntegrityError:
        raise UserExistsError("Error while retrieving user")