from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

app = FastAPI()
Base = declarative_base()


class SecretMessage(BaseModel):
    # Опишите Pydantic-схему для зашифрованных сообщений.
    # Все поля - обязательные.

    title: str = Field(...,)
    message: str = Field(...,)



class ReadyNews(Base):
    # Опишите модель SQLAlchemy для хранения данных в БД.
    # Дополнительных классов создавать не нужно.
    # Таблицу назовите `news`, в ней должен быть столбец id.
    # @declared_attr
    # def __tablename__(cls):
    #     """Именем таблицы будет название модели в нижнем регистре."""
    #     return cls.__name__.lower()
    __tablename__ = 'news'
    # Во все таблицы будет добавлено поле ID.
    id = Column(Integer, primary_key=True)
    title = Column(String)
    message = Column(String)



def decoder(data: dict[str, str]) -> dict[str, str]:
    """
    Сверхсекретный декодер.

    Здесь всё работает, ничего менять не надо!
    """
    decoded_data = {}
    for key, value in data.items():
        decoded_str = (chr(int(chunk)) for chunk in value.split('-'))
        decoded_data[key] = ''.join(decoded_str)
    return decoded_data


@app.post('/super-secret-base')
def reciever(encoded_news: SecretMessage):

    new_news = encoded_news.dict()

    # Передайте сообщение в декодер.
    new_n = decoder(new_news)

    # Создайте переменную ready_news - объект класса ReadyNews
    # из дешифрованного сообщения.
    ready_news = ReadyNews(**new_n)

    # Здесь мог бы быть код, сохраняющий сообщение в базу данных,
    # но его писать не надо.

    # Эндпоинт возвращает объект класса ReadyNews.
    # Здесь ничего менять не надо.
    return ready_news
