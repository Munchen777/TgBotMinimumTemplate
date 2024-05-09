import configparser

from sqlalchemy.ext.asyncio import (async_sessionmaker,
                                    create_async_engine,
                                    AsyncSession)
from dataclasses import dataclass


@dataclass
class BotToken:
    token: str


@dataclass
class Database:
    port: int
    host: str
    database_name: str
    database_user: str
    password: str


@dataclass
class Config:
    tg_bot: BotToken
    db: Database


def load_config(path):
    config = configparser.ConfigParser()
    config.read(path)

    token = config['tg_bot']
    database = config['db']

    return Config(
        tg_bot=BotToken(
            token=token.get('token')),

        db=Database(
            database_name=database.get('POSTGRES_DB'),
            database_user=database.get('POSTGRES_USER'),
            port=database.get('POSTGRES_PORT'),
            host=database.get('POSTGRES_HOST'),
            password=database.get('POSTGRES_PASSWORD')),
    )


config = load_config('.env')
DATABASE_url_async = (f'postgresql+asyncpg://{config.db.database_user}:{config.db.password}'
                      f'@{config.db.host}:{config.db.port}/{config.db.database_name}')

async_engine = create_async_engine(url=DATABASE_url_async, echo=True)
async_session: async_sessionmaker = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
