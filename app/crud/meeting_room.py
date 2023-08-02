# app/crud/meeting_room.py
"""
Получаем объект pydantic, конвертируем в словарь и заносим в бд.

Функция-обработчик будет принимать объект Pydantic-модели MeetingRoomCreate
и возвращать объект ORM-модели MeetingRoom
(она описана в файле app/models/meeting_room.py).
Чтобы передать полученные в запросе данные из
Pydantic-схемы в ORM-модель — потребуется конвертировать схему в словарь.
"""
# Импортируем sessionmaker из файла с настройками БД.
from app.core.db import AsyncSessionLocal
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate


# Функция работает с асинхронной сессией,
# поэтому ставим ключевое слово async.
# В функцию передаём схему MeetingRoomCreate.
async def create_meeting_room(
        new_room: MeetingRoomCreate
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

    # Создаём асинхронную сессию через контекстный менеджер.
    # Чтобы сессия была гарантированно закрыта после использования,
    # даже если в процессе выполнения произойдёт ошибка — подключите её
    # через асинхронный контекстный менеджер
    async with AsyncSessionLocal() as session:
        # Добавляем созданный объект в сессию.
        # Никакие действия с базой пока ещё не выполняются.
        session.add(db_room)

        # Записываем изменения непосредственно в БД.
        # Так как сессия асинхронная, используем ключевое слово await.
        await session.commit()

        # Обновляем объект db_room: считываем данные из БД,
        # чтобы получить его id.
        await session.refresh(db_room)
    # Возвращаем только что созданный объект класса MeetingRoom.
    return db_room
