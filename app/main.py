"""Templates for."""
from fastapi import FastAPI

# Импортируем главный роутер.
from api.routers import main_router
from app.core.config import settings
# Импортируем корутину для создания первого суперюзера.
from app.core.init_db import create_first_superuser

app = FastAPI(title=settings.app_title, description=settings.description)

# Подключаем главный роутер.
app.include_router(main_router)


# При старте приложения запускаем корутину create_first_superuser.
@app.on_event('startup')
async def startup():
    """
    Обработчик событий FastAPI
    Теперь надо вызвать корутину create_first_superuser() при старте
    приложения. Для этого в FastAPI применяется обработчик
    событий @app.on_event('startup'), где app — это объект самого приложения,
    класса FastAPI.
    Разместите такой декоратор над функцией — и эта функция будет
    выполняться каждый раз при перезагрузке или запуске приложения.
    Есть аналогичный обработчик, предназначенный для выполнения действий
    в момент остановки приложения: @app.on_event('shutdown').
    """
    await create_first_superuser()

# kaonashi
# =^..^=______/
