from os import path
import sqlite3
import os
import MoodService.constants as constants


def create_database_if_not_exists():

    print('here')

    if path.exists(constants.database_location):
        return True

    conn = sqlite3.connect(constants.database_location)

    cur = conn.cursor()
    for statement in constants.create_user_table:
        cur.execute(statement)

    conn.commit()
    conn.close()
    return True


def remove_database():

    if path.exists(constants.database_location):
        os.remove(constants.database_location)


