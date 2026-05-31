from fastapi import APIRouter, Depends, HTTPException, status
import sqlite3
from database import get_db
from services import auth_service
from models import user_model

# Инициализация изолированного маршрутизатора API для модуля аутентификации
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(data: auth_service.UserRegisterSchema, db: sqlite3.Connection = Depends(get_db)):
    # Вызов функции бизнес-логики для необратимого хеширования переданного пароля
    hashed = auth_service.hash_password(data.password)
    try:
        # Обращение к слою данных для генерации новой записи в таблице пользователей
        user_model.create_user(db, data.username, hashed)
        return {"message": f"Пользователь {data.username} создан"}
    except sqlite3.IntegrityError:
        # Перехват исключения СУБД при нарушении ограничения UNIQUE для поля username
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Этот логин уже занят. Придумай другой!"
        )


@router.post("/login")
def login(data: auth_service.UserRegisterSchema, db: sqlite3.Connection = Depends(get_db)):
    # Поиск учетной записи пользователя в базе данных по переданному имени (username)
    user = user_model.get_user_by_username(db, data.username)

    # Криптографическая верификация: проверка существования записи и соответствия хэш-значения пароля
    if user and auth_service.verify_password(data.password, user["password_hash"]):
        return {
            "status": "success",
            "message": f"Добро пожаловать, {data.username}!",
            "user_id": user["id"]
        }

    # Генерация исключения со статусом 401 при предоставлении некорректных учетных данных
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный логин или пароль"
    )
