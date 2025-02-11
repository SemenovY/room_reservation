"""
Вообще, в проектах на FastAPI импорты классов через __init__.py —
это частое явление, причем не только в каталогах с моделями или эндпоинтами,
но и в каталогах crud/, schemas/ или в других.
В проекте бронирования переговорок мы не будем переписывать все импорты,
но никто не станет вас удерживать, если вы решите применить
этот подход в своих проектах.
"""
# app/api/endpoints/__init__.py
from .meeting_room import router as meeting_room_router
from .reservation import router as reservation_router
# Как и при импорте моделей в файл app/models/__init__.py, здесь уместно
# применить относительные адреса, а не абсолютные.
# Теперь объекты роутеров будут доступны непосредственно
# из пакета app/api/endpoints.
from .user import router as user_router  # noqa
