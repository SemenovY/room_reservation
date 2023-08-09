"""В начале листинга мы, среди прочего, импортируем три асинхронных генератора:
 get_async_session, get_user_db и get_user_manager; они используются в системе
 Dependency Injection. Так как корутина create_user() будет запускаться при
 старте приложения, а не в результате HTTP-запроса, механизм
 Dependency Injection (DI) мы применить не можем, он тут не сработает.
Использование контекстных менеджеров — это способ получить объекты, которые
в обычной ситуации (при обработке HTTP-запросов) были бы получены через
механизм DI.
"""
import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate

# Превращаем асинхронные генераторы в асинхронные менеджеры контекста.
# Три асинхронных контекстных менеджера подряд служат всего лишь одной
# цели — получить объект класса UserManager и вызвать его метод create().
# Первый контекстный менеджер предоставляет объект асинхронной сессии
# второму контекстному менеджеру, тот, в свою очередь, предоставляет объект
# класса SQLAlchemyUserDatabase (адаптер базы данных) для третьего
# контекстного менеджера. И третий контекстный менеджер уже предоставляет
# доступ к объекту класса UserManager.
get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


# Корутина, создающая юзера с переданным email и паролем.
# Возможно создание суперюзера при передаче аргумента is_superuser=True.
async def create_user(
        email: EmailStr, password: str, is_superuser: bool = False
):
    try:
        # Получение объекта асинхронной сессии.
        async with get_async_session_context() as session:
            # Получение объекта класса SQLAlchemyUserDatabase.
            async with get_user_db_context(session) as user_db:
                # Получение объекта класса UserManager.
                async with get_user_manager_context(user_db) as user_manager:
                    # Создание пользователя.
                    await user_manager.create(
                        UserCreate(
                            email=email, 
                            password=password, 
                            is_superuser=is_superuser
                        )
                    )
    # В случае, если такой пользователь уже есть, ничего не предпринимать.
    except UserAlreadyExists:
        pass


# Корутина, проверяющая, указаны ли в настройках данные для суперюзера.
# Если да, то вызывается корутина create_user для создания суперпользователя.
async def create_first_superuser():
    if (settings.first_superuser_email is not None 
            and settings.first_superuser_password is not None):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )
