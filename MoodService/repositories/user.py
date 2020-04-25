import sqlite3
import MoodService.constants as constants
from MoodService.objects.user import User
database_created = False


def _get_connection():
    """Returns a database connection"""
    return sqlite3.connect(constants.database_location)


def get_user_by_id(user_name: str) -> User:
    """Returns a user object from the database by id"""
    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE user_name = ?",
                (user_name,))
    result = cur.fetchone()
    conn.close()

    if result is not None:
        return User(result[0], result[1], result[2])


def create_new_user(user_name: str, password_hash: str) -> int:
    """Returns the int_id (primary key) of a newly created user"""
    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO users (user_name, password_hash) VALUES (?,?)",
                (user_name, password_hash))
    conn.commit()
    conn.close()

    return cur.lastrowid