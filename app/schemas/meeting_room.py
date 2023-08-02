"""Модели для переговорки, для Post and Get запросов."""
from typing import Optional

from pydantic import BaseModel, Field


class MeetingRoomCreate(BaseModel):
    """Модель переговорки, для Post запроса, название обязательно."""

    name: str = Field(
        ..., min_length=1, max_length=100,
        title='Название переговорки', description='Можно в любом регистре'
    )
    description: Optional[str]
