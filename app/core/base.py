"""
Миграции
Чтобы Alembic увидел изменения в моделях, нужно импортировать новую
модель в файле app/core/base.py. Иначе в миграции ничего не отобразится.
Импорты класса Base и всех моделей для Alembic.
"""
from app.core.db import Base  # noqa
from app.models.meeting_room import MeetingRoom  # noqa
from app.models.reservation import Reservation  # noqa
