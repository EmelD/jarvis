import asyncio
import logging
import signal
from aiogram import Bot, Dispatcher
from jarvis.bot.handlers import router
from jarvis.core.settings import bot_settings


mcp_manager = None


async def on_startup(bot: Bot):
    logging.info("Starting bot: resources initialisation...")

    logging.info("Starting bot: Initializing MCP connections...")
    # if mcp_manager:
    #     await mcp_manager.start_all()
    logging.info("Starting bot: MCP connections has been initialized!")

    await bot.send_message(bot_settings.ADMIN_ID, "🚀 Bot successfully launched after deployment!")


async def on_shutdown(bot: Bot):
    logging.info("Stopping bot: Cleaning Resources...")

    await bot.send_message(bot_settings.ADMIN_ID, "⚠️ Bot is stopping (deployment finish).")

    logging.info("Stopping bot: Closing MCP connections...")
    # if mcp_manager:
    #     await mcp_manager.stop_all()
    logging.info("Stopping bot: MCP connections has been closed!")

    logging.info("Stopping bot: Closing Bot session...")
    await bot.session.close()
    logging.info("Stopping bot: Bot session has been closed...")


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    bot = Bot(token=bot_settings.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(router)

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(dp.stop_polling()))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot is stopped")
