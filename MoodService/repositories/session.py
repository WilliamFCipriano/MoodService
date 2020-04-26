from MoodService.repositories.sqlite_util import get_connection
from MoodService.objects.session import Session
from MoodService.exceptions.session import SessionNotFoundException


def get_session_by_token(token: str) -> Session:
    """Returns a session objects for any given token, raises
    SessionNotFoundException when the session does not exist"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM sessions WHERE token = ?", (token,))
    result = cur.fetchone()
    conn.close()

    if result is None:
        raise(SessionNotFoundException)

    return Session(result[1], result[0], result[2])


def create_session(user_int_id: int, token: str) -> Session:
    """Creates a session for a given user_int_id and returns it"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO sessions (user_int_id, token) VALUES (?, ?)",
                (user_int_id, token))
    session = Session(user_int_id, cur.lastrowid, token)
    conn.commit()
    conn.close()
    return session
