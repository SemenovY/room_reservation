"""Templates for."""
from fastapi import FastAPI

# Импортируем главный роутер.
from api.routers import main_router
from app.core.config import settings

app = FastAPI(title=settings.app_title, description=settings.description)

# Подключаем главный роутер.
app.include_router(main_router)

# kaonashi
# =^..^=______/
