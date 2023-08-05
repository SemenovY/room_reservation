"""Модели для бронирования переговорок, дата и время, номер комнаты."""
from sqlalchemy import Column, DateTime, ForeignKey, Integer

from app.core.db import Base


class Reservation(Base):
    """Модель для бронирования."""
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    # Столбец с внешним ключом: ссылка на таблицу meetingroom.
    meetingroom_id = Column(Integer, ForeignKey('meetingroom.id'))
