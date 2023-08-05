"""Pydantic схемы для переговорки, для Post and Get запросов."""
from typing import Optional

from pydantic import BaseModel, Field, validator


class MeetingRoomBase(BaseModel):
    """Создадим базовый класс схемы комнаты."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


class MeetingRoomCreate(MeetingRoomBase):
    """Схема переговорки, для Post запроса, название обязательно."""

    name: str = Field(
        ..., min_length=1, max_length=100,
        title='Название переговорки', description='Можно в любом регистре'
    )


class MeetingRoomUpdate(MeetingRoomBase):
    """
    Обновлять можно каждое поле в отдельности или оба поля сразу.

    Поэтому переопределять свойства полей не надо, тело класса оставим пустым,
    напишем pass.
    """

    @validator('name')
    def name_cannot_be_null(cls, value: str):
        """Create test for None value."""
        if value is None:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value


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
