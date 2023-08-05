"""Pydantic схемы для резервирования времени, для Post and Get запросов."""
from datetime import datetime

from pydantic import BaseModel, root_validator, validator


class ReservationBase(BaseModel):
    """Создадим базовый класс схемы резерва комнаты."""

    from_reserve: datetime
    to_reserve: datetime


class ReservationUpdate(ReservationBase):
    """
    Обновлять нужно оба поля сразу.
    """
    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value):
        """Проверяем чтобы время брони было не меньше текущего."""
        if value <= datetime.now():
            raise ValueError(
                'Время начала бронирования '
                'не может быть меньше текущего времени'
            )
        return value

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        """Сравниваем время начало и окончания резерва."""
        if values['from_reserve'] >= values['to_reserve']:
            raise ValueError(
                'Время начала бронирования '
                'не может быть больше времени окончания'
            )
        return values


class ReservationCreate(ReservationUpdate):
    """Схема бронирования, для Post запроса, название обязательно."""

    meetingroom_id: int


class ReservationDB(ReservationBase):
    """Возвращаем ответ после создания комнаты."""

    id: int
    meetingroom_id: int

    class Config:
        """
        Чтобы FastAPI мог сериализовать объект ORM-модели.

        В схему MeetingRoomDB, нужно указать, что схема может принимать
        на вход объект базы данных, а не только Python-словарь или JSON-объект.
        """

        orm_mode = True
