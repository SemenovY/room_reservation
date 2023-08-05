"""
Создаем «объединяющей» роутер,
к которому будут подключены все нужные роутеры. И тогда в файле app/main.py
можно будет одной строкой подключить этот главный роутер.
В файле app/api/routers.py создайте главный роутер с именем main_router
и подключите к нему существующие роутеры из app/api/endpoints.
Объекты роутеров называются одинаково, router, так что при помощи
конструкции from ... import ... as ... присвоим им псевдонимы (alias).
"""
# app/api/routers.py
from fastapi import APIRouter

# Две длинных строчки импортов заменяем на одну короткую.
from app.api.endpoints import meeting_room_router, reservation_router


main_router = APIRouter()
main_router.include_router(
    meeting_room_router, prefix='/meeting_rooms', tags=['Meeting Rooms']
)
main_router.include_router(
    reservation_router, prefix='/reservations', tags=['Reservations']
)

# Из файла app/api/routers.py можно управлять тегами и префиксами роутеров:
# их можно указывать не только в объекте APIRouter,
# но и в методе include_router.
# Перенесём теги и префикс роутера meeting_room_router из
# файла app/api/endpoints/meeting_room.py в app/api/routers.py.
