"""Модели для переговорки, для Post and Get запросов."""
from typing import Optional

from pydantic import BaseModel, Field


# Базовый класс схемы, от которого наследуем все остальные.
class MeetingRoomBase(BaseModel):
    """Создадим базовый класс модели комнаты."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


class MeetingRoomCreate(MeetingRoomBase):
    """Модель переговорки, для Post запроса, название обязательно."""

    name: str = Field(
        ..., min_length=1, max_length=100,
        title='Название переговорки', description='Можно в любом регистре'
    )


class MeetingRoomDB(MeetingRoomCreate):
    """Возвращаем ответ после создания комнаты."""

    id: int

    class Config:
        """
        Чтобы FastAPI мог сериализовать объект ORM-модели.

        В схему MeetingRoomDB, нужно указать, что схема может принимать
        на вход объект базы данных, а не только Python-словарь или JSON-объект.
        """

        orm_mode = True
