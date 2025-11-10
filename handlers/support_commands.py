# handlers/support_commands.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from texts.messages import ABOUT_RESPONSE

router = Router()

# Клавиатура для раздела "О боте"
about_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🌍 Наш канал", url="https://t.me/daily_annet"),
            InlineKeyboardButton(text="💌 Поддержка", url="https://t.me/ConnectKeks_bot")
        ],
        [
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")
        ]
    ]
)

@router.callback_query(F.data == "about")
async def show_about(callback: CallbackQuery):
    """Показывает информацию о боте"""
    try:
        await callback.message.edit_text(
            ABOUT_RESPONSE,
            parse_mode="HTML",
            reply_markup=about_kb,
            disable_web_page_preview=True
        )
    except Exception as e:
        # Если не получается отредактировать сообщение - отправляем новое
        await callback.message.answer(
            ABOUT_RESPONSE,
            parse_mode="HTML",
            reply_markup=about_kb,
            disable_web_page_preview=True
        )
    await callback.answer()

# Обработчик для возврата в главное меню
@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    from handlers.start import main_menu_kb, WELCOME_TEXT
    try:
        await callback.message.edit_text(
            WELCOME_TEXT,
            parse_mode="HTML",
            reply_markup=main_menu_kb
        )
    except:
        await callback.message.answer(
            WELCOME_TEXT,
            parse_mode="HTML",
            reply_markup=main_menu_kb
        )
    await callback.answer()