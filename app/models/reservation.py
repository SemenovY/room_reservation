"""Модели для бронирования переговорок, дата и время, номер комнаты."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer

from app.core.db import Base


class Reservation(Base):
    """Модель для бронирования."""
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    # Столбец с внешним ключом: ссылка на таблицу meetingroom.
    meetingroom_id = Column(Integer, ForeignKey('meetingroom.id'))
    # Каскадное удаление объектов бронирования при удалении связанного с ними
    # пользователя не требуется: удаление пользователей мы отключили.
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return (
            f'Уже забронировано с {self.from_reserve} по {self.to_reserve}'
        )
