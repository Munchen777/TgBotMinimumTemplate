import asyncio


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode

from config.config import config, async_engine
from config.models import Base
from my_logger import my_logger
from utils.set_bot_commands import set_commands


bot = Bot(token=config.tg_bot.token)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        my_logger.error("Таблицы в базе данных PostgreSQL удалены.")
        await conn.run_sync(Base.metadata.create_all)
        my_logger.success("Таблицы в базе данных PostgreSQL созданы.")


async def main():
    my_logger.info("Бот запускается.")
    await set_commands(bot=bot)

    await create_tables()

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot, close_bot_session=True)
    finally:
        my_logger.stop("Бот остановился.")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
