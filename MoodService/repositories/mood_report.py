from MoodService.objects.mood_report import MoodReport
from MoodService.repositories.sqlite_util import get_connection
from MoodService.exceptions.mood_report import MoodAlreadySubmittedException
import datetime


def new_mood_report(user_id, mood) -> None:
    """saves a new mood report, if a mood report has already been
     submitted today it raises MoodAlreadySubmittedException"""
    conn = get_connection()
    cur = conn.cursor()

    # check to see if the user has already submitted a mood today.
    cur.execute("SELECT * FROM mood_report WHERE date = ? AND user_id = ?",
                (datetime.datetime.now().date(), user_id))

    if not len(cur.fetchall()) >= 1:
        # deduplication of mood values, unique index prevents duplicates
        cur.execute("INSERT OR IGNORE INTO mood_values (value) VALUES (?)", (mood,))

        # getting the id of the newly or previously inserted value as RETURNING is not supported.
        cur.execute("SELECT id FROM mood_values WHERE value = ?", (mood,))
        mood_value_id = cur.fetchone()[0]

        cur.execute("INSERT INTO mood_report (mood_value_id, user_id, date) VALUES (?,?,?)",
                        (mood_value_id, user_id, datetime.datetime.now().date()))

        conn.commit()
        conn.close()
    else:
        conn.close()
        raise MoodAlreadySubmittedException()