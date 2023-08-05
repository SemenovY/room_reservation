"""
Теперь опишем эндпоинт для операции Create.

Для подключения эндпоинтов создадим роутер,
затем подключим его к объекту приложения.
Функция-обработчик будет использовать асинхронную функцию
create_meeting_room() и поэтому сама тоже должна быть асинхронной:
в ней тоже нужно применить ключевые слова async и await.
"""
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
# Вместо импортов 6 функций импортируйте объект meeting_room_crud.
from app.crud.meeting_room import meeting_room_crud
from app.schemas.meeting_room import (
    MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate
)
from app.api.validators import check_meeting_room_exists, check_name_duplicate

router = APIRouter()


@router.post(
    '/',
    # Указываем схему ответа.
    # Не выводим пустые поля и дефолт.
    # Исключать значение по умолчанию
    # response_model_exclude_defaults=True,
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,

)
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate,
        # Указываем зависимость, предоставляющую объект сессии,
        # как параметр функции.
        session: AsyncSession = Depends(get_async_session),
):
    """
    Создаем новую комнату.
    Роутер подключим его к объекту приложения.
    Вызываем функцию проверки уникальности поля name:
    """
    await check_name_duplicate(meeting_room.name, session)
    # Замените вызов функции на вызов метода.
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room


@router.get(
    '/',
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True,
)
async def get_all_meeting_rooms(
        session: AsyncSession = Depends(get_async_session)
):
    """Для гет запроса на возврат всех комнат."""
    # Замените вызов функции на вызов метода.
    all_rooms = await meeting_room_crud.get_multi(session)
    return all_rooms


@router.patch(
    # ID обновляемого объекта будет передаваться path-параметром.
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def partially_update_meeting_room(
        # ID обновляемого объекта.
        meeting_room_id: int,
        # JSON-данные, отправленные пользователем.
        obj_in: MeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Обновляем объект в базе, роутер path.

    Получаем объект из БД по ID.
    В ответ ожидается либо None, либо объект класса MeetingRoom.
    Выносим повторяющийся код в отдельную корутину.
    Если в запросе получено поле name — проверяем его на уникальность.
    Передаём в корутину все необходимые для обновления данные.
    """
    meeting_room = await check_meeting_room_exists(meeting_room_id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    # Замените вызов функции на вызов метода.
    meeting_room = await meeting_room_crud.update(
        meeting_room, obj_in, session
    )
    return meeting_room


@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def remove_meeting_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Удаляем комнату, по id.
    Выносим повторяющийся код в отдельную корутину.
    """
    meeting_room = await check_meeting_room_exists(meeting_room_id, session)
    # Замените вызов функции на вызов метода.
    meeting_room = await meeting_room_crud.remove(meeting_room, session)
    return meeting_room
