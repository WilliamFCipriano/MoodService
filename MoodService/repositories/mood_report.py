from datetime import datetime, timedelta, date
from MoodService.repositories.sqlite_util import get_connection
from MoodService.exceptions.mood_report import MoodAlreadySubmittedException
from MoodService.exceptions.mood_report import PercentileMatrixNotInitializedException


def new_mood_report(user_id: int, mood: str) -> None:
    """saves a new mood report, if a mood report has already been
     submitted today it raises MoodAlreadySubmittedException"""
    conn = get_connection()
    cur = conn.cursor()

    current_date = datetime.now().date()

    # check to see if the user has already submitted a mood today.
    cur.execute("SELECT COUNT(*) FROM mood_report WHERE date = ? AND user_id = ?",
                (current_date, user_id))

    if not cur.fetchone()[0] >= 1:
        # deduplication of mood values, unique index prevents duplicates
        cur.execute("INSERT OR IGNORE INTO mood_values (value) VALUES (?)", (mood,))

        # getting the id of the newly or previously inserted value as RETURNING is not supported.
        cur.execute("SELECT id FROM mood_values WHERE value = ?", (mood,))
        mood_value_id = cur.fetchone()[0]

        cur.execute("INSERT INTO mood_report (mood_value_id, user_id, date) VALUES (?,?,?)",
                        (mood_value_id, user_id, current_date))

        cur.execute("UPDATE users SET last_submission = ? WHERE int_id = ?", (current_date, user_id))

        conn.commit()
        conn.close()
    else:
        conn.close()
        raise MoodAlreadySubmittedException()


def historical_mood_report(user_id: int, mood: str, date: date, streak: int) -> None:
    """saves a historical mood report, for testing purposes does not do any sanity checks"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO mood_values (value) VALUES (?)", (mood,))

    cur.execute("SELECT id FROM mood_values WHERE value = ?", (mood,))
    mood_value_id = cur.fetchone()[0]

    cur.execute("INSERT INTO mood_report (mood_value_id, user_id, date) VALUES (?,?,?)",
                    (mood_value_id, user_id, date))

    cur.execute("UPDATE users SET last_submission = ? AND streak_days = ? WHERE int_id = ?", (date, streak, user_id))

    conn.commit()
    conn.close()


def get_streak_eligible_user_totals() -> list:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT streak_days FROM users WHERE last_submission >= ? ORDER BY streak_days desc",
                (datetime.now().date() - timedelta(days=1),))
    result = cur.fetchall()
    conn.close()

    return result


def save_percentile_data(percentile_data: dict) -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM mood_percentiles")

    for percentile in percentile_data:
        cur.execute("INSERT INTO mood_percentiles (streak_days, percentile) VALUES (?,?)",
                    (percentile_data[percentile], percentile))

    conn.commit()
    conn.close()


def get_percentile_for_streak(streak: int) -> float:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT percentile FROM mood_percentiles WHERE streak_days = ? ORDER BY percentile desc", (streak,))
    result = cur.fetchone()
    conn.close()

    if result is not None:
        return result[0]
    else:
        raise PercentileMatrixNotInitializedException
