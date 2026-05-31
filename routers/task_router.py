from fastapi import APIRouter, Depends, HTTPException, status
import sqlite3
from typing import Optional
from database import get_db
from services.task_service import TaskCreateSchema
from models import task_model

# Инициализация маршрутизатора API для управления сущностями задач
router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("")
def get_tasks(status: Optional[str] = None, priority: Optional[str] = None, db: sqlite3.Connection = Depends(get_db)):
    # Запрос к слою данных для извлечения списка задач с учетом переданных фильтров
    tasks = task_model.get_filtered_tasks(db, status, priority)
    # Преобразование объектов sqlite3.Row в стандартные словари Python для сериализации в JSON
    return [dict(t) for t in tasks]

@router.post("")
def create_task(task: TaskCreateSchema, db: sqlite3.Connection = Depends(get_db)):
    # Делегация операции создания записи в базе данных соответствующей функции модели
    task_model.add_task(db, task.user_id, task.title, task.priority)
    return {"message": "Задача добавлена по всем канонам профи!"}

@router.patch("/{task_id}")
def update_task_status(task_id: int, new_status: str, db: sqlite3.Connection = Depends(get_db)):
    # Частичное обновление (модификация) атрибута статуса конкретной задачи
    task_model.update_status(db, task_id, new_status)
    return {"message": "Статус обновлен"}

@router.patch("/{task_id}/edit")
def edit_task(task_id: int, new_title: str, db: sqlite3.Connection = Depends(get_db)):
    # Частичное обновление текстового содержимого (заголовка) задачи по её идентификатору
    task_model.update_title(db, task_id, new_title)
    return {"message": "Название задачи изменено"}

@router.delete("/{task_id}")
def delete_task(task_id: int, db: sqlite3.Connection = Depends(get_db)):
    # Верификация существования целевой записи в базе данных перед выполнением операции удаления
    if not task_model.get_task_by_id(db, task_id):
        # Генерация HTTP-исключения со статусом 404 в случае отсутствия объекта
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача №{task_id} не найдена. Удалять нечего!"
        )
    # Физическое удаление записи из таблицы при успешном прохождении проверки
    task_model.delete_task_by_id(db, task_id)
    return {"message": "Задача успешно удалена"}