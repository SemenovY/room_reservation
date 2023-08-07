"""
Миграции
Чтобы Alembic увидел изменения в моделях, нужно импортировать новую
модель в файле app/core/base.py. Иначе в миграции ничего не отобразится.
Импорты класса Base и всех моделей для Alembic.
"""
# app/core/base.py
# Импортируйте модель User и в файл app/core/base.py для Alembic. Все модели
# теперь доступны из файла app/models/__init__.py, так что для чистоты кода
# перепишем здесь импорты моделей в одну строку:
"""Импорты класса Base и всех моделей для Alembic."""
from app.core.db import Base  # noqa
from app.models import MeetingRoom, Reservation, User  # noqa
