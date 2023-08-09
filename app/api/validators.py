
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
# Так как в Python-пакете app.models модели импортированы в __init__.py,
# импортировать их можно прямо из пакета.
from app.models import MeetingRoom, Reservation, User


async def check_name_duplicate(
        # Корутина, проверяющая уникальность полученного имени переговорки.
        room_name: str,
        session: AsyncSession,
) -> None:
    """Проверка в базе на совпадение имен."""
    # Замените вызов функции на вызов метода.
    room_id = await meeting_room_crud.get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )


async def check_meeting_room_exists(
    # Оформляем повторяющийся код в виде отдельной корутины.
    meeting_room_id: int,
    session: AsyncSession,
) -> MeetingRoom:
    """
    Отдельная функция для проверки повторяющегося id.
    :param meeting_room_id:
    :param session:
    """
    # Замените вызов функции на вызов метода.
    meeting_room = await meeting_room_crud.get(meeting_room_id, session)
    if meeting_room is None:
        raise HTTPException(status_code=404, detail='Переговорка не найдена!')
    return meeting_room


async def check_reservation_intersections(**kwargs) -> None:
    """
    Этот валидатор должен:
    принимать неопределенный список ключевых аргументов **kwargs;
    вызывать метод get_reservations_at_the_same_time()
    объекта reservation_crud, при вызове метода передавать в него
    распакованный **kwargs, результат вызова должен быть присвоен
    переменной reservations;
    если список reservations непустой — выбрасывать исключение
    HTTPException со статусом 422 и в сообщении об ошибке возвращать
    полученный список объектов;
    если список reservations пустой — ничего возвращать не надо.
    """
    reservations = await reservation_crud.get_reservations_at_the_same_time(
        **kwargs
    )
    if reservations:
        raise HTTPException(status_code=422, detail=str(reservations))


async def check_reservation_before_edit(
        reservation_id: int,
        session: AsyncSession,
        user: User,
) -> Reservation:
    """
    Будем проверять, существует ли запрошенный объект бронирования,
    а чуть позже добавим к нему условия, связанные с пользователями.
    """
    reservation = await reservation_crud.get(
        # Для понятности кода можно передавать аргументы по ключу.
        obj_id=reservation_id, session=session
    )
    if not reservation:
        raise HTTPException(status_code=404, detail='Бронь не найдена!')
    if reservation.user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail='Невозможно редактировать или удалить чужую бронь!'
        )
    return reservation
