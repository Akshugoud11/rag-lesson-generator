
import sqlite3
from pathlib import Path

# Database file location
DB_PATH = Path(__file__).with_name("lesson_memory.db")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    return connection


def create_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lesson_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            lesson TEXT,
            verdict TEXT,
            criteria TEXT,
            feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

    print("SQLite database table created successfully!")


if __name__ == "__main__":
    create_table()
