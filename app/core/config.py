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
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        """
        Подкласс Config содержит специальный атрибут env_file.

        В нём нужно указать имя файла с переменными окружения;
        полный путь прописывать не обязательно.
        """

        env_file = '.env'


settings = Settings()
