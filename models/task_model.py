
import sqlite3
from typing import Optional


def get_filtered_tasks(db: sqlite3.Connection, status: Optional[str], priority: Optional[str]):
    # Условие 'WHERE 1=1' применяется для динамического формирования SQL-запроса через конъюнкцию (AND)
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []

    # Добавление фильтрации по статусу задачи при наличии параметра
    if status:
        query += " AND status = ?"
        params.append(status)

    # Добавление фильтрации по приоритету задачи при наличии параметра
    if priority:
        query += " AND priority = ?"
        params.append(priority)

    # Выполнение параметризованного запроса для предотвращения SQL-инъекций
    return db.execute(query, params).fetchall()


def get_task_by_id(db: sqlite3.Connection, task_id: int):
    # Поиск идентификатора задачи для верификации её существования в базе данных
    return db.execute("SELECT id FROM tasks WHERE id = ?", (task_id,)).fetchone()


def add_task(db: sqlite3.Connection, user_id: int, title: str, priority: str):
    # Инициализация новой записи в таблице tasks с указанием внешнего ключа пользователя
    db.execute("INSERT INTO tasks (user_id, title, priority) VALUES (?, ?, ?)", (user_id, title, priority))
    # Фиксация внесенных изменений в транзакции
    db.commit()


def update_status(db: sqlite3.Connection, task_id: int, status: str):
    # Модификация атрибута status для указанного идентификатора задачи
    db.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    db.commit()


def update_title(db: sqlite3.Connection, task_id: int, title: str):
    # Обновление строкового значения заголовка (title) задачи
    db.execute("UPDATE tasks SET title = ? WHERE id = ?", (title, task_id))
    db.commit()


def delete_task_by_id(db: sqlite3.Connection, task_id: int):
    # Удаление записи из таблицы tasks по первичному ключу
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
