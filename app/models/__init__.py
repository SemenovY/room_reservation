"""
При использовании модели MeetingRoom в её атрибуте
reservations = relationship('Reservation', ...) вызывается модель Reservation ,
а SQLAlchemy ничего не знает об этой модели.
Есть как минимум два способа решения этой проблемы; мы применим первый из них.
1. Импорт моделей в __init__
Прежде чем работать с пакетом, интерпретатор считывает содержимое
файла __init__.py. Этим можно воспользоваться: в файле __init__.py
«сообщим» интерпрертатору о модели Reservation до того, как он приступит
к выполнению кода.
"""
from .meeting_room import MeetingRoom
from .reservation import Reservation
# app/models/__init__.py
# Чтобы SQLAlchemy узнала обо всех моделях до того, как начнутся выстраиваться
# взаимосвязи между ними, импортируйте модель User в
# файл app/models/__init__.py:
from .meeting_room import MeetingRoom
from .reservation import Reservation
from .user import User
