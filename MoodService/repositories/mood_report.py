from MoodService.objects.mood_report import MoodReport
from MoodService.repositories.sqlite_util import get_connection
from MoodService.exceptions.mood_report import MoodAlreadySubmittedException
import datetime


def new_mood_report(user_id, mood) -> None:
    """saves a new mood report, if a mood report has already been
     submitted today it raises MoodAlreadySubmittedException"""
    conn = get_connection()
    cur = conn.cursor()

    current_date = datetime.datetime.now().date()

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


def historical_mood_report(user_id, mood, date) -> None:
    """saves a historical mood report, for testing purposes does not do any sanity checks"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO mood_values (value) VALUES (?)", (mood,))

    cur.execute("SELECT id FROM mood_values WHERE value = ?", (mood,))
    mood_value_id = cur.fetchone()[0]

    cur.execute("INSERT INTO mood_report (mood_value_id, user_id, date) VALUES (?,?,?)",
                    (mood_value_id, user_id, date))

    conn.commit()
    conn.close()

