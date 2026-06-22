import sqlite3
from pathlib import Path


DATABASE_PATH = (
    Path(__file__).parent /
    "skilltwin_memory.db"
)


def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    return connection
def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_memory (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT UNIQUE,

            goal TEXT,

            completed_tasks TEXT,

            observations TEXT
        )
        """
    )

    connection.commit()

    connection.close()