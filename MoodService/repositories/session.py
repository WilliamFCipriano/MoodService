import sqlite3
import MoodService.constants as constants
from MoodService.objects.session import Session
from MoodService.exceptions.session import SessionNotFoundException


def _get_connection():
    """Returns a database connection"""
    return sqlite3.connect(constants.database_location)


def get_session_by_token(token) -> Session:
    """Returns a session objects for any given token, raises
    SessionNotFoundException when the session does not exist"""
    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM sessions WHERE token = ?", (token,))
    result = cur.fetchone()
    conn.close()

    if result is None:
        raise(SessionNotFoundException,
              "Session was not located for that token")

    return Session(result[1], result[0])


def create_session(user_int_id, token) -> Session:
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO sessions (user_int_id, token) VALUES (?, ?)",
                (user_int_id, token))
    conn.commit()
    conn.close()

    return Session(user_int_id, cur.lastrowid)