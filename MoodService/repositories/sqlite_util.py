from os import path
import sqlite3
import os
import MoodService.constants as constants


def _database_exists() -> bool:
    """checks to see if a file exists at a certain path"""
    return path.exists(constants.database_location)


def create_database_if_not_exists() -> None:
    """creates a database if one does not already exist"""
    if _database_exists():
        return

    conn = sqlite3.connect(constants.database_location)
    cur = conn.cursor()

    for statement in constants.create_user_table:
        cur.execute(statement)

    for statement in constants.create_session_table:
        cur.execute(statement)

    for statement in constants.create_mood_tables:
        cur.execute(statement)

    conn.commit()
    conn.close()


def remove_database() -> None:
    """removes the database from the disk (for unit testing purposes)"""
    if _database_exists():
        os.remove(constants.database_location)