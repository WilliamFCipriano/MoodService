from os import path
import sqlite3
import os
import MoodService.constants as constants


def _database_exists() -> bool:
    return path.exists(constants.database_location)


def create_database_if_not_exists() -> None:
    if _database_exists():
        return True

    conn = sqlite3.connect(constants.database_location)
    cur = conn.cursor()

    for statement in constants.create_user_table:
        cur.execute(statement)

    for statement in constants.create_session_table:
        cur.execute(statement)

    conn.commit()
    conn.close()


def remove_database() -> None:
    if _database_exists():
        os.remove(constants.database_location)