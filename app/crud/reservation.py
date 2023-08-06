"""
Теперь мы для любой новой модели можем сразу подключить пять CRUD-методов,
создав объект класса CRUDBase и передав в него нужную модель.
Если для какой-то модели нужно реализовать уникальные методы, которые
неприменимы к другим моделям — создаём класс-наследник базового класса,
добавляем в него нужный метод — и создаём объект уже
на основе этого нового класса.
"""
from datetime import datetime

from sqlalchemy import and_, between, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.reservation import Reservation


class CRUDReservation(CRUDBase):
    """
    Создаём класс CRUDReservation (наследник CRUDBase).
    Расширяем этот класс методом get_reservations_at_the_same_time();
    этот метод проверяет, свободен ли запрошенный интервал времени;
    если это время полностью или частично зарезервировано в каких-то
    объектах бронирования — метод возвращает список этих объектов.
    """
    async def get_reservations_at_the_same_time(
            self,
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            session: AsyncSession,
    ) -> list[Reservation]:
        """
        Метод будет искать в модели Reservation объекты,
        которые пересекаются по времени с интервалом,
        указанном в запросе — и возвращать список найденных объектов
        """
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == meetingroom_id,
                and_(
                    from_reserve <= Reservation.to_reserve,
                    to_reserve >= Reservation.from_reserve
                )
            )
        )
        reservations = reservations.scalars().all()
        return reservations


# Создаём объекта класса CRUDReservation.
reservation_crud = CRUDReservation(Reservation)
