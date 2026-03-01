from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import init_db
from app.routers.todo import router as todo_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация при запуске приложения."""
    # Инициализация БД
    await init_db()
    yield
    # Закрытие при остановке (если нужно)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Асинхронное TODO API на FastAPI + SQLAlchemy + PostgreSQL",
    lifespan=lifespan,
)

# Подключение роутов
app.include_router(todo_router, prefix="/api/v1")

# Подключение статики
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Главная страница с фронтендом."""
    static_path = Path(__file__).parent / "static" / "index.html"
    return static_path.read_text(encoding="utf-8")


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения."""
    return {"status": "healthy"}
