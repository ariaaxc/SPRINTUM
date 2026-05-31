import sqlite3
from config import DB_NAME

def get_connection():
    # Создание прямого соединения с БД для административных скриптов (init_db.py)
    connection = sqlite3.connect(DB_NAME)
    # Активация поддержки ограничений внешних ключей в SQLite
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection

def get_db():
    # Создание сессии подключения к БД для маршрутов FastAPI (генератор yield)
    conn = sqlite3.connect(DB_NAME)
    # Активация каскадных операций удаления для контроля целостности данных
    conn.execute("PRAGMA foreign_keys = ON;")
    # Настройка фабрики строк для доступа к полям выборки по их именам
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        # Гарантированное закрытие соединения по завершении HTTP-запроса
        conn.close()

