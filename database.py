import sqlite3
import logging
# from datetime import datetime
from pathlib import Path


class Database:
    def __init__(self, db_path='hangman_bot.db'):
        self.db_path = Path(db_path)
        self.init_db()

    def init_db(self):
        """Инициализация базы данных и создание таблиц"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                '''
                )
                cursor.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS word_categories (
                        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        description TEXT
                    )
                '''
                )

        except sqlite3.Error as e:
            logging.error(f"Ошибка инициализации БД: {e}")
