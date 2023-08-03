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


# Асинхронный генератор сессий.
async def get_async_session():
    """
    Создадим функцию, которая будет использоваться как зависимость.

    Эта функция должна открывать сессии, а после выполнения всех операций,
    использующих эту сессию, или при ошибке — закрывать её.
    Чтобы зависимость выполнила какие-то действия после окончания обработки
    HTTP-запроса (в нашем случае — закрыла сессию), применяют ключевое
    слово yield.
    Асинхронная функция, в которой содержится ключевое слово yield,
    называется «асинхронным генератором».
    """
    # Через асинхронный контекстный менеджер и sessionmaker
    # открывается сессия.
    async with AsyncSessionLocal() as async_session:
        # Генератор с сессией передается в вызывающую функцию.
        yield async_session
        # Когда HTTP-запрос отработает - выполнение кода вернётся сюда,
        # и при выходе из контекстного менеджера сессия будет закрыта.
