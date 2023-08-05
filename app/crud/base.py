"""Чтобы не дублировать код — для CRUD-операций создадим базовый класс
с набором стандартных методов; унаследуем от него конкретные классы
для CRUD-операций с определёнными моделями.
А обращаться будем уже не к функциям, а к методам этого класса.
"""
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    """
    Базовый класс.
    """
    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession,):
        """Функция для получения объекта по его ID."""
        # Вызываем функцию проверки уникальности поля name:
        db_obj = await session.execute(select(self.model).where(
            self.model.id == obj_id
        ))
        # Извлекаем из него конкретное значение.
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession,):
        """
        Асинхронная функция, которая будет считывать из базы все переговорки.
        """
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(self, obj_in, session: AsyncSession,):
        """
        Получаем объект джейсончик, вся работа через асинхронку.

        Сначала конвертируем в обычный словарь.
        Затем работа с базой данных.
        """
        # Конвертируем объект в словарь.
        # может быть превращён в словарь методом Pydantic-модели.
        obj_in_data = obj_in.dict()
        # Создаём объект модели MeetingRoom.
        # В параметры передаём пары "ключ=значение",
        # для этого распаковываем словарь.
        db_obj = self.model(**obj_in_data)
        # Записываем изменения непосредственно в БД.
        # Так как сессия асинхронная, используем ключевое слово await.
        session.add(db_obj)
        await session.commit()
        # Обновляем объект db_room: считываем данные из БД,
        # чтобы получить его id.
        await session.refresh(db_obj)
        # Возвращаем только что созданный объект класса MeetingRoom.
        return db_obj

    async def update(self, db_obj, obj_in, session: AsyncSession,):
        """
        Обновляем.
        """
        # Представляем объект из БД в виде словаря.
        obj_data = jsonable_encoder(db_obj)
        # Конвертируем объект с данными из запроса в словарь,
        # исключаем неустановленные пользователем поля.
        update_data = obj_in.dict(exclude_unset=True)
        # Перебираем все ключи словаря, сформированного из БД-объекта.
        for field in obj_data:
            # Если конкретное поле есть в словаре с данными из запроса,
            if field in update_data:
                # то устанавливаем объекту БД новое значение атрибута.
                setattr(db_obj, field, update_data[field])
        # Добавляем обновленный объект в сессию.
        session.add(db_obj)
        # Фиксируем изменения.
        await session.commit()
        # Обновляем объект из БД.
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj, session: AsyncSession,):
        """
        удаляем комнату.
        """
        # Удаляем объект из БД.
        await session.delete(db_obj)
        # Фиксируем изменения в БД.
        await session.commit()
        # Не обновляем объект через метод refresh(),
        # следовательно, он всё ещё содержит информацию об удаляемом объекте.
        return db_obj

    # async def get_by_attribute(
    #         self,
    #         attr_name: str,
    #         attr_value: str,
    #         session: AsyncSession,
    # ):
    #     """
    #     Список методов можно дополнять или изменять по своему усмотрению,
    #     например, вместо метода get() можно реализовать метод
    #     get_by_attribute(), который по произвольному атрибуту
    #     (в том числе и по id) сможет получить объект из базы.
    #     """
    #     attr = getattr(self.model, attr_name)
    #     db_obj = await session.execute(
    #         select(self.model).where(attr == attr_value)
    #     )
    #     return db_obj.scalars().first()
