# handlers/tarot.py
from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from texts.messages import TAROT_INTRO  # ← используем твой текст
from services.tarot_service import get_random_tarot

router = Router()

# Кнопки под картой дня
tarot_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📣 Подписаться на канал", url="https://t.me/your_channel")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")]
    ]
)

# Кнопка для получения карты
get_card_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🃏 Узнать карту дня", callback_data="show_tarot_card")]
    ]
)

@router.callback_query(lambda c: c.data == "tarot_card")
async def ask_for_tarot(callback: CallbackQuery):
    await callback.message.answer(
        TAROT_INTRO,
        reply_markup=get_card_kb,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "show_tarot_card")
async def send_tarot_card(callback: CallbackQuery):
    try:
        photo, text = get_random_tarot()
        await callback.message.answer_photo(
            photo=photo,
            caption=text,
            parse_mode="HTML",
            reply_markup=tarot_menu_kb
        )
    except Exception as e:
        await callback.message.answer("Произошла ошибка при загрузке карты. Попробуйте позже.")
        print(f"Ошибка: {e}")
    await callback.answer()