"""
Теперь мы для любой новой модели можем сразу подключить пять CRUD-методов,
создав объект класса CRUDBase и передав в него нужную модель.
Если для какой-то модели нужно реализовать уникальные методы, которые
неприменимы к другим моделям — создаём класс-наследник базового класса,
добавляем в него нужный метод — и создаём объект уже
на основе этого нового класса.
"""
from datetime import datetime

from typing import Optional
from sqlalchemy import and_, between, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.reservation import Reservation
from app.models.user import User


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
            # Добавляем звёздочку, чтобы обозначить, что все дальнейшие параметры
            # должны передаваться по ключу. Это позволит располагать
            # параметры со значением по умолчанию перед параметрами без таких значений.
            *,
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            # Добавляем новый опциональный параметр - id объекта бронирования.
            reservation_id: Optional[int] = None,
            session: AsyncSession,
    ) -> list[Reservation]:
        """
        Метод будет искать в модели Reservation объекты,
        которые пересекаются по времени с интервалом,
        указанном в запросе — и возвращать список найденных объектов
        При обновлении объекта бронирования надо удостовериться, что
        изменённый интервал времени не пересечётся с забронированными
        интервалами, при этом надо исключить из проверки сам
        модифицируемый объект модели. Для этого в запрос к базе
        нужно передать id объекта бронирования.
        """
        # Выносим уже существующий запрос в отдельное выражение.
        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )
        # Если передан id бронирования...
        if reservation_id is not None:
            # ... то к выражению нужно добавить новое условие.
            select_stmt = select_stmt.where(
                # id искомых объектов не равны id обновляемого объекта.
                Reservation.id != reservation_id
            )
        # Выполняем запрос.
        reservations = await session.execute(select_stmt)
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_reservations_for_room(
            self,
            room_id: int,
            session: AsyncSession,
    ):
        """
        Запрос к БД должен извлекать все объекты Reservation,
        которые связаны с запрошенной переговоркой; время окончания
        бронирования у этих объектов должно быть больше текущего времени.
        """
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meetingroom_id == room_id,
                Reservation.to_reserve > datetime.now()
            )
        )
        reservations = reservations.scalars().all()
        return reservations

    async def get_by_user(
            self,
            user: User,
            session: AsyncSession,
    ):
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.user_id == user.id,
            )
        )
        reservations = reservations.scalars().all()
        return reservations

    async def get_count_res_at_the_same_time(
            self,
            from_reserve: datetime,
            to_reserve: datetime,
            session: AsyncSession,
    ) -> list[dict[str, int]]:
        reservations = await session.execute(
            # Получаем количество бронирований переговорок за период
            select([Reservation.meetingroom_id,
                    func.count(Reservation.meetingroom_id)]).where(
                Reservation.from_reserve >= from_reserve,
                Reservation.to_reserve <= to_reserve
            ).group_by(Reservation.meetingroom_id)
        )
        reservations = reservations.scalars().all()
        return reservations


# Создаём объекта класса CRUDReservation.
reservation_crud = CRUDReservation(Reservation)
