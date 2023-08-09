"""Описание моделей проекта."""
from sqlalchemy import Column, String, Text # noqa
# атрибут relationship, описывающий взаимосвязи между моделями,
# по которому можно будет получить все объекты бронирования
# для данной переговорки
from sqlalchemy.orm import relationship

from app.core.db import Base


class MeetingRoom(Base):
    """
    Модель переговорки.

    Имя переговорки должно быть не больше 100 символов, уникальным и непустым.
    """

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    # Установите связь между моделями через функцию relationship.
    reservations = relationship('Reservation', cascade='delete')
    # Теперь при удалении объекта переговорки SQLAlchemy удалит
    # все объекты бронирования, связанные с этой переговоркой.
