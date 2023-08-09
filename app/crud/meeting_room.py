"""
Получаем объект pydantic, конвертируем в словарь и заносим в бд.

Функция-обработчик будет принимать объект Pydantic-модели MeetingRoomCreate
и возвращать объект ORM-модели MeetingRoom
(она описана в файле app/models/meeting_room.py).
Чтобы передать полученные в запросе данные из
Pydantic-схемы в ORM-модель — потребуется конвертировать схему в словарь.
"""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.meeting_room import MeetingRoom


# Создаем новый класс, унаследованный от CRUDBase.
class CRUDMeetingRoom(CRUDBase):

    # Преобразуем функцию в метод класса.
    async def get_room_id_by_name(
            # Дописываем параметр self.
            # В качестве альтернативы здесь можно
            # применить декоратор @staticmethod.
            self,
            room_name: str,
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
        db_room_id = db_room_id.scalars().first()
        return db_room_id


# Объект crud наследуем уже не от CRUDBase,
# а от только что созданного класса CRUDMeetingRoom.
# Для инициализации передаем модель, как и в CRUDBase.
meeting_room_crud = CRUDMeetingRoom(MeetingRoom)
