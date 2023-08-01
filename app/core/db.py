"""Настройки для подключения к базе данных."""
# Все классы и функции для асинхронной работы
# находятся в модуле sqlalchemy.ext.asyncio.
# Добавляем импорт классов для определения столбца ID.
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """
    Чтобы не повторяться в описании каждой модели — расширьте базовый класс.

    Приватный атрибут __tablename__ и поле ID создаются автоматически.
    """

    @declared_attr
    def __tablename__(cls):
        """Именем таблицы будет название модели в нижнем регистре."""
        return cls.__name__.lower()

    # Во все таблицы будет добавлено поле ID.
    id = Column(Integer, primary_key=True)


# В качестве основы для базового класса укажем класс PreBase.
Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
