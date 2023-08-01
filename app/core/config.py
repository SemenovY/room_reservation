"""
В директории проекта /app каталог /core (в переводе с английского — «ядро»).

Будет хранить файлы, отвечающие за «ядро» проекта — общие настройки приложения,
файлы для работы с БД и другие файлы, отвечающие за конфигурацию проекта.
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    BaseSettings.

    Позволяет считывать из операционной системы переменные
    окружения, напрямую обращаться к файлу .env.
    """

    # app_author: str
    # db_url: str = 'postgres://login:password@127.0.0.1:5432/room_reservation'
    # path: str
    app_title: str = 'Бронирование переговорок'
    description: str = 'API для возможности забронировать переговорку'
    database_url: str

    class Config:
        """
        Подкласс Config содержит специальный атрибут env_file.

        В нём нужно указать имя файла с переменными окружения;
        полный путь прописывать не обязательно.
        """

        env_file = '.env'


settings = Settings()

# kaonashi
# =^..^=______/
