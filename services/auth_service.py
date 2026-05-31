import hashlib
import os
from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    username: str
    password: str


def hash_password(password: str) -> str:
    # Генерация случайной криптографической соли (16 байт)
    salt = os.urandom(16)
    # Создание надежного хэша по стандарту PBKDF2
    db_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # Сохраняем в виде строки: соль и хэш в шестнадцатеричном формате через разделитель
    return f"{salt.hex()}:{db_hash.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # Извлекаем сохраненную соль и хэш из строки базы данных
        salt_hex, db_hash_hex = hashed_password.split(":")
        salt = bytes.fromhex(salt_hex)

        # Хешируем введенный пароль с той же самой солью
        new_hash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)
        # Сравниваем полученный хэш с тем, что лежит в базе
        return new_hash.hex() == db_hash_hex
    except Exception:
        return False
