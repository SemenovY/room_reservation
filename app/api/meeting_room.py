"""
Теперь опишем эндпоинт для операции Create.

Для подключения эндпоинтов создадим роутер,
затем подключим его к объекту приложения.
Функция-обработчик будет использовать асинхронную функцию
create_meeting_room() и поэтому сама тоже должна быть асинхронной:
в ней тоже нужно применить ключевые слова async и await.
"""
# Импортируем асинхронный генератор сессий.
from app.core.db import get_async_session
from app.crud.meeting_room import create_meeting_room, get_room_id_by_name, read_all_rooms_from_db
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomDB
from fastapi import APIRouter, Depends, HTTPException

# Импортируем класс асинхронной сессии для аннотации параметра.
from sqlalchemy.ext.asyncio import AsyncSession


# Добавьте параметр prefix.
router = APIRouter(
    prefix='/meeting_rooms',
    tags=['Meeting Rooms']
)

# В пути /meeting_rooms/ стоит закрывающий слеш, и это неспроста:
# позже мы опишем эндпоинты для обновления и удаления объектов,
# и в адресе будет указываться ID переговорки:
# /meeting_rooms/{meeting_room_id}.
# Эндпоинт /meeting_rooms/ будет расширен, это не «окончательный» путь;
# в таком случае нужно ставить закрывающий слеш.


@router.post(
    '/',
    # Указываем схему ответа.
    response_model=MeetingRoomDB,
    # Не выводим пустые поля и дефолт
    response_model_exclude_none=True,
    # Исключать значение по умолчанию
    # response_model_exclude_defaults=True,
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
    """
    # Вторым параметром передаём сессию в CRUD-функцию:
    # Вызываем функцию проверки уникальности поля name:

    room_id = await get_room_id_by_name(meeting_room.name, session)
    # Если такой объект уже есть в базе - вызываем ошибку:

    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )
    # Вторым параметром передаём сессию в CRUD-функцию:
    new_room = await create_meeting_room(meeting_room, session)
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
    all_rooms = await read_all_rooms_from_db(session)
    return all_rooms
