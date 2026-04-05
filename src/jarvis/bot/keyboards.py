from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard():
    buttons = [
        [KeyboardButton(text="📅 План на сегодня")],
        [KeyboardButton(text="✅ Задачи Todoist")],
        [KeyboardButton(text="🔍 Обзор чатов Telegram")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
