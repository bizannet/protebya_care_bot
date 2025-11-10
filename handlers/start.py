# handlers/start.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from texts.messages import WELCOME_TEXT
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from texts.messages import WELCOME_TEXT
router = Router()


main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📅 Прогноз на день", callback_data="daily_forecast"),
            InlineKeyboardButton(text="🃏 Карта дня", callback_data="tarot_card")
        ],
        [InlineKeyboardButton(text="🌙 Фаза Луны", callback_data="moon_phase")],
        [InlineKeyboardButton(text="🔢 Нумерологический расчёт", callback_data="numerology")],
        [InlineKeyboardButton(text="❤️ О боте", callback_data="about")],

    ]
)

@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb, parse_mode="HTML")

@router.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(WELCOME_TEXT, reply_markup=main_menu_kb, parse_mode="HTML")
    await callback.answer()