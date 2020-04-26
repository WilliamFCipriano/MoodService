from datetime import datetime, timedelta
from MoodService.repositories.sqlite_util import get_connection
from MoodService.objects.user import User
database_created = False


def get_user_by_id(user_name: str) -> User:
    """Returns a user object from the database by id"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE user_name = ?",
                (user_name,))
    result = cur.fetchone()
    conn.close()

    if result is not None:
        return User(result[0], result[1], result[2], result[3], result[4])


def create_new_user(user_name: str, password_hash: str) -> int:
    """Returns the int_id (primary key) of a newly created user"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO users (user_name, password_hash) VALUES (?,?)",
                (user_name, password_hash))
    conn.commit()
    conn.close()

    return cur.lastrowid


def get_user_streak_length(user_int_id: int) -> int:
    """Calculates the current users streak in days"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT date FROM mood_report where user_id = ? ORDER BY date desc", (user_int_id,))
    dates = cur.fetchall()

    streak_days = 0
    x = 0

    for date in dates:
        if date[0] == str(datetime.now().date() - timedelta(days=x)):
            streak_days += 1
        else:
            break
        x += 1

    cur.execute("UPDATE users SET streak_days = ? WHERE int_id = ?", (streak_days, user_int_id))
    conn.commit()
    conn.close()

    return streak_days
