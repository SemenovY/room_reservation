# app/crud/meeting_room.py
"""
Получаем объект pydantic, конвертируем в словарь и заносим в бд.

Функция-обработчик будет принимать объект Pydantic-модели MeetingRoomCreate
и возвращать объект ORM-модели MeetingRoom
(она описана в файле app/models/meeting_room.py).
Чтобы передать полученные в запросе данные из
Pydantic-схемы в ORM-модель — потребуется конвертировать схему в словарь.
"""
from typing import Optional
# Добавляем к списку импортов импорт jsonable_encoder.
from fastapi.encoders import jsonable_encoder
# Добавляем импорт функции select.
from sqlalchemy import select
# Импортируем класс асинхронной сессии для аннотаций.
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


# Функция работает с асинхронной сессией,
# поэтому ставим ключевое слово async.
# В функцию передаём схему MeetingRoomCreate.
async def create_meeting_room(
        new_room: MeetingRoomCreate,
        # Добавляем новый параметр.
        session: AsyncSession,
) -> MeetingRoom:
    """
    Получаем объект джейсончик, вся работа через асинхронку.

    Сначала конвертируем в обычный словарь.
    Затем работа с базой данных.

    """
    # Конвертируем объект MeetingRoomCreate в словарь.
    # может быть превращён в словарь методом Pydantic-модели.
    new_room_data = new_room.dict()
    # Создаём объект модели MeetingRoom.
    # В параметры передаём пары "ключ=значение",
    # для этого распаковываем словарь.
    db_room = MeetingRoom(**new_room_data)
    session.add(db_room)
    # Записываем изменения непосредственно в БД.
    # Так как сессия асинхронная, используем ключевое слово await.
    await session.commit()
    # Обновляем объект db_room: считываем данные из БД,
    # чтобы получить его id.
    await session.refresh(db_room)
    # Возвращаем только что созданный объект класса MeetingRoom.
    return db_room


# Добавляем новую асинхронную функцию.
async def get_room_id_by_name(
        room_name: str,
        # Добавляем новый параметр.
        session: AsyncSession,
) -> Optional[int]:
    """
    Проверяем уникальность имени переговорки.

    Добавьте в файл app/crud/meeting_room.py асинхронную
    функцию get_room_id_by_name(), которая примет на вход имя переговорки
    (поле name из полученного запроса).
    Если в базе будет найден объект с таким же name — функция вернёт id
    этого объекта; возвращать весь объект целиком нет смысла, ведь
    цель — просто узнать, есть ли в базе такой объект.
    Если в базе нет одноимённой переговорки — функция вернёт None.
    """
    db_room_id = await session.execute(
        select(MeetingRoom.id).where(
            MeetingRoom.name == room_name
        )
    )
    # Извлекаем из него конкретное значение.
    db_room_id = db_room_id.scalars().first()
    return db_room_id


async def read_all_rooms_from_db(
        session: AsyncSession,
) -> list[MeetingRoom]:
    """Асинхронная функция, которая будет считывать из базы все переговорки."""
    db_rooms = await session.execute(select(MeetingRoom))
    return db_rooms.scalars().all()


async def get_meeting_room_by_id(
        room_id: int,
        session: AsyncSession,
) -> Optional[MeetingRoom]:
    """Функция для получения объекта по его ID."""
    # Вызываем функцию проверки уникальности поля name:
    db_room = await session.execute(
        select(MeetingRoom).where(
            MeetingRoom.id == room_id
        )
    )
    # Извлекаем из него конкретное значение.
    db_room = db_room.scalars().first()
    return db_room


async def update_meeting_room(
        # Объект из БД для обновления.
        db_room: MeetingRoom,
        # Объект из запроса.
        room_in: MeetingRoomUpdate,
        session: AsyncSession,
) -> MeetingRoom:
    # Представляем объект из БД в виде словаря.
    obj_data = jsonable_encoder(db_room)
    # Конвертируем объект с данными из запроса в словарь,
    # исключаем неустановленные пользователем поля.
    update_data = room_in.dict(exclude_unset=True)
    # Перебираем все ключи словаря, сформированного из БД-объекта.
    for field in obj_data:
        # Если конкретное поле есть в словаре с данными из запроса, то...
        if field in update_data:
        # ...устанавливаем объекту БД новое значение атрибута.
            setattr(db_room, field, update_data[field])
    # Добавляем обновленный объект в сессию.
    session.add(db_room)
    # Фиксируем изменения.
    await session.commit()
    # Обновляем объект из БД.
    await session.refresh(db_room)
    return db_room
