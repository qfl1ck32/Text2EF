import sqlite3
import os
import os.path as path

from constants import constants
from logger import logger


def create_database():

    for file_name in os.listdir(constants.DATABASES_PATH):
        os.remove(path.join(constants.DATABASES_PATH, file_name))

    for file_name in os.listdir(constants.DATASET_DATABASE_PATH):
        database_path = f"{path.join(constants.DATABASES_PATH, file_name)}.db"

        connection = sqlite3.connect(database_path)

        folder_path = os.path.join(
            constants.DATASET_DATABASE_PATH, file_name)

        sql_file_path = f"{folder_path}/schema.sql"

        if os.path.exists(sql_file_path):
            logger.info(f"Creating database for {file_name}")

            try:
                connection.executescript(open(sql_file_path, "r").read())
            except sqlite3.Error as e:
                logger.error(f"Error creating database for {file_name}: {e}")
                continue

    connection.commit()
    connection.close()


if __name__ == '__main__':
    create_database()
