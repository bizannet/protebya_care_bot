# handlers/moon.py
from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from services.moon_service import get_current_moon_phase
from texts.moon.phases import MOON_PHASE_TEXTS

router = Router()

moon_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")]
    ]
)

@router.callback_query(lambda c: c.data == "moon_phase")
async def send_moon_phase(callback: CallbackQuery):
    try:
        phase_key = get_current_moon_phase()
        text = MOON_PHASE_TEXTS.get(phase_key, "Не удалось определить фазу Луны.")
        await callback.message.answer(text, parse_mode="HTML", reply_markup=moon_kb)
    except Exception as e:
        await callback.message.answer(
            "Произошла ошибка при определении фазы Луны. Попробуйте позже.",
            reply_markup=moon_kb
        )
    await callback.answer()