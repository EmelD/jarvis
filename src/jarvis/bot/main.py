import asyncio
import logging
from aiogram import Bot, Dispatcher
from jarvis.bot.handlers import router
from jarvis.core.settings import bot_settings


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=bot_settings.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    logging.info("Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
