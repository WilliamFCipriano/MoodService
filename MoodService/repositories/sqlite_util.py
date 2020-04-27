from os import path
import sqlite3
import os
import MoodService.constants as constants
import MoodService.services.audit as audit

log = audit.get_logger('sqlite_util')


def get_connection():
    """Returns a database connection"""
    return sqlite3.connect(constants.database_location)


def _database_exists() -> bool:
    """Checks to see if a file exists at a certain path"""
    return path.exists(constants.database_location)


def create_database_if_not_exists() -> None:
    """Creates a database if one does not already exist, then
    populates all the tables."""
    log.info("Creating new database if one does not already exist")
    if _database_exists():
        return

    conn = sqlite3.connect(constants.database_location)
    cur = conn.cursor()

    log.info("Creating user table")
    for statement in constants.create_user_table:
        cur.execute(statement)

    log.info("Creating session table")
    for statement in constants.create_session_table:
        cur.execute(statement)

    log.info("Creating mood table")
    for statement in constants.create_mood_tables:
        cur.execute(statement)

    log.info("Creating mood percentile table")
    for statement in constants.create_mood_percentile_tables:
        cur.execute(statement)

    log.info("Committing and closing database")
    conn.commit()
    conn.close()


def remove_database() -> None:
    """Removes the database from the disk (for unit testing purposes)"""
    log.info("Removing database")
    if _database_exists():
        os.remove(constants.database_location)