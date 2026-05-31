import sqlite3

def get_user_by_username(db: sqlite3.Connection, username: str):
    # Поиск записи в таблице users по уникальному строковому идентификатору (username)
    return db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

def create_user(db: sqlite3.Connection, username: str, password_hash: str):
    # Внесение новой учетной записи пользователя с сохранением защищенного хэша пароля
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
    # Подтверждение транзакции и фиксация изменений в базе данных
    db.commit()
