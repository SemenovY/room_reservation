"""
В файле app/api/endpoints/reservation.py создайте «пустой» роутер
для модели Reservation.
Здесь создаем обработку запросов на резервирование перегородок.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Дополнительно импортируем новый валидатор:
from app.api.validators import (
    check_meeting_room_exists,
    check_reservation_before_edit,
    check_reservation_intersections,
)
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.reservation import reservation_crud
from app.models import User
from app.schemas.reservation import (ReservationCreate, ReservationDB,
                                     ReservationUpdate
                                     )


router = APIRouter()


@router.post(
    '/',
    # Эндпоинт должен возвращать объект, описываемый схемой ReservationDB.
    response_model=ReservationDB
    # Обратите внимание: в декораторе не применён аргумент
    # response_model_exclude_none=True,
    # ведь у объектов Reservation нет опциональных полей.
)
async def create_reservation(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_async_session),
    # Получаем текущего пользователя и сохраняем в переменную user.
    user: User = Depends(current_user),
):
    """
    В теле корутины последовательно должны вызываться проверки:
    что указанная в запросе переговорка вообще существует,
    что запрошенный интервал не пересекается по времени с ранее созданными
    объектами Reservation — здесь аргументы нужно передавать с указанием
    ключей, так как валидатор принимает kwargs.
    """
    # Проверка, что указанная в запросе переговорка вообще существует
    await check_meeting_room_exists(reservation.meetingroom_id, session)
    # Проверка, что запрошенный интервал не пересекается по времени с ранее
    # созданными объектами Reservation — здесь аргументы нужно передавать
    # с указанием ключей, так как валидатор принимает kwargs.
    await check_reservation_intersections(
        # Так как валидатор принимает **kwargs,
        # аргументы должны быть переданы с указанием ключей.
        **reservation.dict(), session=session
    )
    new_reservation = await reservation_crud.create(
        # Передаём объект пользователя в метод создания объекта бронирования.
        reservation, session, user
    )
    return new_reservation


@router.get(
    '/',
    response_model=list[ReservationDB]
)
async def get_all_reservations(
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список бронирования."""
    reservations = await reservation_crud.get_multi(session)
    return reservations


@router.delete(
    '/{reservation_id}',
    response_model=ReservationDB
)
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Удаляем бронь."""
    reservation = await check_reservation_before_edit(reservation_id, session)
    reservation = await reservation_crud.remove(reservation, session)
    return reservation


@router.patch(
    '/{reservation_id}',
    response_model=ReservationDB
)
async def update_reservation(
    reservation_id: int,
    obj_in: ReservationUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Обновляем бронь."""
    # Проверяем, что такой объект бронирования вообще существует.
    reservation = await check_reservation_before_edit(reservation_id, session)
    # Проверяем, что нет пересечений с другими бронированиями.
    await check_reservation_intersections(
        # Новое время бронирования, распакованное на ключевые аргументы.
        **obj_in.dict(),
        # id обновляемого объекта бронирования,
        reservation_id=reservation_id,
        # id переговорки.
        meetingroom_id=reservation.meetingroom_id,
        session=session
    )
    reservation = await reservation_crud.update(
        db_obj=reservation,
        # На обновление передаем объект класса ReservationUpdate,
        # как и требуется.
        obj_in=obj_in,
        session=session,
    )
    return reservation
