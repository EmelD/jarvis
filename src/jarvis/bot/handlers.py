from aiogram import Router, types, F
from aiogram.filters import Command

from jarvis.apps.agents import jarvis_agent
from jarvis.bot.keyboards import get_main_keyboard


router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я твой AI-ассистент с MCP-инструментами. Чем помочь?",
        reply_markup=get_main_keyboard()
    )


@router.message(F.text == "📅 План на сегодня")
async def handle_today_plan(message: types.Message):
    response = await jarvis_agent.graph.ainvoke({"messages": [("user", "Расскажи мои планы из календаря на сегодня")]})
    await message.answer("Запрашиваю данные из Google Calendar... ⏳")

    await message.answer("У вас 2 встречи: в 14:00 Sync и в 16:00 Code Review.")


@router.message()
async def handle_any_message(message: types.Message):
    """Обработка произвольного текстового запроса через Агента"""
    user_input = message.text
    await message.answer(f"Вы спросили: {user_input}. Агент обрабатывает запрос...")
    result = await jarvis_agent.graph.ainvoke({"messages": [("user", user_input)]})
    reply = result["messages"][-1].content
