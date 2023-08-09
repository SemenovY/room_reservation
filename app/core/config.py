"""
В директории проекта /app каталог /core (в переводе с английского — «ядро»).

Будет хранить файлы, отвечающие за «ядро» проекта — общие настройки приложения,
файлы для работы с БД и другие файлы, отвечающие за конфигурацию проекта.
"""
from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """
    BaseSettings.

    Позволяет считывать из операционной системы переменные
    окружения, напрямую обращаться к файлу .env.
    """

    app_title: str = 'Бронирование переговорок'
    description: str = 'API для возможности забронировать переговорку'
    database_url: str
    secret: str = 'SECRET'
    # Немного модифицируем пример из документации и настроим проект так,
    # чтобы при запуске приложения создавался суперюзер, если его еще нет
    # в системе.
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        """
        Подкласс Config содержит специальный атрибут env_file.

        В нём нужно указать имя файла с переменными окружения;
        полный путь прописывать не обязательно.
        """

        env_file = '.env'


settings = Settings()
