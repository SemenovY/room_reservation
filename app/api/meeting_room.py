"""
Теперь опишем эндпоинт для операции Create.

Для подключения эндпоинтов создадим роутер,
затем подключим его к объекту приложения.
Функция-обработчик будет использовать асинхронную функцию
create_meeting_room() и поэтому сама тоже должна быть асинхронной:
в ней тоже нужно применить ключевые слова async и await.
"""
from app.crud.meeting_room import create_meeting_room
from app.schemas.meeting_room import MeetingRoomCreate
from fastapi import APIRouter

router = APIRouter()

# В пути /meeting_rooms/ стоит закрывающий слеш, и это неспроста:
# позже мы опишем эндпоинты для обновления и удаления объектов,
# и в адресе будет указываться ID переговорки:
# /meeting_rooms/{meeting_room_id}.
# Эндпоинт /meeting_rooms/ будет расширен, это не «окончательный» путь;
# в таком случае нужно ставить закрывающий слеш.


@router.post('/meeting_rooms/')
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate,
):
    """
    Создаем новую комнату.

    Роутер подключим его к объекту приложения.
    """
    new_room = await create_meeting_room(meeting_room)
    return new_room
