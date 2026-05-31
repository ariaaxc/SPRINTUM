from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

# Импорт модулей маршрутизации для авторизации и управления задачами
from routers import auth_router, task_router

# Инициализация основного экземпляра приложения FastAPI с указанием метаданных
app = FastAPI(title="Sprintum API", version="1.0.0")

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="."), name="static")

# Настройка промежуточного слоя CORS для разрешения кросс-доменных запросов со всех источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Интеграция изолированных роутеров в общую структуру маршрутов приложения
app.include_router(auth_router.router)
app.include_router(task_router.router)

@app.get("/", response_class=FileResponse)
def read_index():
    # Определение абсолютного пути к текущей директории исполняемого файла
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Возврат статического HTML-файла фронтенда по корневому адресу
    return os.path.join(current_dir, "index.html")

