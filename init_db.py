# init_db.py
import sqlite3
from database import get_connection


def init_database():
    print("Инициализация базы данных...")

    try:
        # Использование менеджера контекста (with) для автоматического закрытия соединения
        with get_connection() as connection:
            cursor = connection.cursor()

            # Создание таблицы пользователей users с ограничением UNIQUE для поля username
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Создание таблицы задач tasks с ограничением внешнего ключа FOREIGN KEY и каскадным удалением
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title VARCHAR(100) NOT NULL,
                    description TEXT,
                    status VARCHAR(20) DEFAULT 'todo',
                    priority VARCHAR(10) DEFAULT 'medium',
                    due_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')

            # Фиксация изменений (commit) происходит автоматически при успешном выходе из блока with
            print("База данных успешно создана и настроена!")

    except sqlite3.Error as error:
        # Перехват и логирование исключений, возникших при работе с СУБД SQLite
        print(f"Ошибка при работе с SQLite: {error}")


if __name__ == "__main__":
    # Точка входа для ручного запуска инициализации базы данных из консоли
    init_database()
