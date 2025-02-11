"""
Теперь все новые модели нужно будет импортировать в файл app/core/base.py.

Вся работа будет вестись в директории /app,
а в настройки Alembic при добавлении новых моделей больше ничего дописывать
не потребуется.
"""
import asyncio
import os
from logging.config import fileConfig

from dotenv import load_dotenv # noqa
from sqlalchemy import engine_from_config  # noqa
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine  # noqa
from sqlalchemy.ext.asyncio import async_engine_from_config  # noqa

from alembic import context
from app.core.base import Base # noqa

# Загрузим файл .env в переменные окружения.
# Библиотека python-dotenv умеет находить файл в «вышестоящих» каталогах,
# поэтому полный путь указывать не обязательно.
load_dotenv('.env')

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Установим для переменной sqlalchemy.url значение из нашего .env файла.
config.set_main_option('sqlalchemy.url', os.environ['DATABASE_URL'])

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# Присвоим переменной target_metadata объект класса MetaData из Base.
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # Всё это можно сделать при помощи batch-операций (групповых операций).
        # Чтобы Alembic сгенерировал такую миграцию, нужно немного
        # поменять настройки.
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
