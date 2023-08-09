"""Pydantic схемы для резервирования времени, для Post and Get запросов."""
from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Extra, Field, root_validator, validator


FROM_TIME = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    """Создадим базовый класс схемы резерва комнаты."""

    from_reserve: datetime = Field(..., example=FROM_TIME)
    to_reserve: datetime = Field(..., example=TO_TIME)

    class Config:
        """
        Чтобы запретить пользователю передавать параметры,
        не описанные в схеме, в подклассе Config устанавливается
        значение extra = Extra.forbid.
        """

        extra = Extra.forbid
        # Теперь схемы, унаследованные от ReservationBase, не будут
        # принимать параметры, которые не описаны в схеме.
        # extra = Extra.forbid — крайне полезный атрибут, который
        # делает поведение API более понятным для пользователя и
        # позволяет бороться со случайными опечатками при передаче параметров.


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
        """Сравниваем время начала и окончания резерва."""
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
    """
    Возвращаем ответ после создания комнаты.
    Чтобы id пользователя возвращался в ответе на запрос, нужно дополнить
    схему ReservationDB. В базе уже могут быть объекты бронирования
    без id пользователя, так что сделаем новое поле схемы опциональным.

    """

    id: int
    meetingroom_id: int
    # Добавьте опциональное поле user_id.
    user_id: Optional[int]

    class Config:
        """
        Чтобы FastAPI мог сериализовать объект ORM-модели.

        В схему MeetingRoomDB, нужно указать, что схема может принимать
        на вход объект базы данных, а не только Python-словарь или JSON-объект.
        """

        orm_mode = True
