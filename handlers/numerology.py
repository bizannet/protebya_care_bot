# handlers/numerology.py
import os
import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
from services.calculator import (
    calculate_day_number,
    calculate_personality,
    # calculate_spirituality,
    # calculate_career,
    # calculate_health,
    # reduce_number
)
from texts.messages import DAILY_FORECAST_INTRO, NUMEROLOGY_INTRO
from texts.day_numbers import (
    DAY_NUMBER_1, DAY_NUMBER_2, DAY_NUMBER_3, DAY_NUMBER_4,
    DAY_NUMBER_5, DAY_NUMBER_6, DAY_NUMBER_7, DAY_NUMBER_8, DAY_NUMBER_9
)

router = Router()


# 2. КЛАССЫ СОСТОЯНИЙ: Оставляем старые и добавляем новый
class DailyForecastStates(StatesGroup):
    waiting_for_birth_date = State()


# 3. НОВЫЙ КЛАСС СОСТОЯНИЯ: Для расчета личности
class PersonalityCalculation(StatesGroup):
    waiting_for_birth_date = State()


# 4. КЛАВИАТУРЫ: Оставляем старую и добавляем новые
forecast_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Проверить другую дату", callback_data="change_birth_date")],
        [InlineKeyboardButton(text="🏠 Вернуться в главное меню", callback_data="back_to_main")]
    ]
)

# 5. НОВЫЕ КЛАВИАТУРЫ: Для расчета личности
personality_calc_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✨ Рассчитать", callback_data="calculate_personality")]
    ]
)

after_calculation_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Вернуться в главное меню", callback_data="back_to_main")]
    ]
)

# 6. ХРАНИЛИЩА: Оставляем как есть
user_daily_forecast_data = {}


# 🔥 ИСПРАВЛЕННЫЙ КОНВЕРТЕР: Без тега <br>!
def md_to_html(text: str) -> str:
    """Конвертирует базовый Markdown в HTML для Telegram (БЕЗ <br>!)"""
    # Убираем возврат каретки
    text = text.replace('\r', '')

    # Жирный: **текст** → <b>текст</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Курсив: *текст* → <i>текст</i>
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)\*(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
    # Моноширинный: `код` → <code>код</code>
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    # Заголовки → жирный
    text = re.sub(r'^#{1,3}\s*(.*?)$', r'<b>\1</b>', text, flags=re.MULTILINE)
    # Списки → эмодзи + отступ
    text = re.sub(r'^\*\s+(.*)$', r'• \1', text, flags=re.MULTILINE)
    # Горизонтальные линии → эмодзи
    text = re.sub(r'^-{3,}$', '⎯⎯⎯', text, flags=re.MULTILINE)
    # Экранирование спецсимволов
    text = text.replace('&', '&amp;').replace('<', '<').replace('>', '>')

    # 🔥 КРИТИЧЕСКИ ВАЖНО: НЕ ИСПОЛЬЗУЕМ <br>!
    # Telegram не поддерживает этот тег в HTML-режиме
    # Вместо этого оставляем обычные переносы строк
    return text.strip()


# 7. ФУНКЦИИ: Оставляем как есть
def validate_date(date_str: str) -> bool:
    """Проверяет корректность даты"""
    try:
        if len(date_str) != 10:
            return False
        if date_str[2] != '.' or date_str[5] != '.':
            return False
        day, month, year = map(int, date_str.split('.'))
        datetime(year=year, month=month, day=day)
        return True
    except (ValueError, TypeError):
        return False


def get_day_text(number: int) -> str:
    """Возвращает текст для дневного числа"""
    texts = {
        1: DAY_NUMBER_1, 2: DAY_NUMBER_2, 3: DAY_NUMBER_3, 4: DAY_NUMBER_4,
        5: DAY_NUMBER_5, 6: DAY_NUMBER_6, 7: DAY_NUMBER_7, 8: DAY_NUMBER_8, 9: DAY_NUMBER_9,
    }
    return texts.get(number, "Неизвестное число дня.")


def get_number_image_path(day_number: int) -> str:
    """Путь к изображению дневного числа"""
    return os.path.join("images/daynumbers", f"{day_number}.jpg")


# --- СИСТЕМА: РАСЧЁТ ЛИЧНОСТИ (1-22) ---
# 8. ОБНОВЛЁННЫЙ ОБРАБОТЧИК ДЛЯ КНОПКИ "НУМЕРОЛОГИЯ"
@router.callback_query(lambda c: c.data == "numerology")
async def start_numerology(callback: CallbackQuery, state: FSMContext):
    """Начало работы с нумерологией - показываем только личность"""
    await callback.message.answer(
        NUMEROLOGY_INTRO,  # Используем существующий текст
        parse_mode="HTML",
        reply_markup=personality_calc_kb
    )
    await callback.answer()


# 9. НОВЫЙ ОБРАБОТЧИК: Запрос даты для расчета личности
@router.callback_query(lambda c: c.data == "calculate_personality")
async def request_birth_date(callback: CallbackQuery, state: FSMContext):
    """Запрос даты рождения для расчета личности"""
    await callback.message.answer(
        "Введите вашу дату рождения в формате <b>ДД.ММ.ГГГГ</b>",
        parse_mode="HTML"
    )
    await state.set_state(PersonalityCalculation.waiting_for_birth_date)
    await callback.answer()


# 10. ИСПРАВЛЕННЫЙ ОБРАБОТЧИК: Обработка даты для расчета личности
@router.message(PersonalityCalculation.waiting_for_birth_date)
async def process_personality_date(message: Message, state: FSMContext):
    """Обработка введенной даты для расчета личности"""
    birth_date = message.text.strip()

    if not validate_date(birth_date):
        await message.answer(
            "❌ Неверный формат даты.\n"
            "Пожалуйста, введите дату как <b>дд.мм.гггг</b>, например:\n"
            "<code>16.02.1995</code>",
            parse_mode="HTML"
        )
        return

    day = int(birth_date[:2])
    personality_number = calculate_personality(day)

    # Читаем .md файлы
    file_path = f"texts/numbers/personality/{personality_number}.md"

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            personality_desc = md_to_html(md_content)
        except Exception as e:
            personality_desc = f"Ошибка при загрузке описания: {str(e)}"
    else:
        # Пытаемся найти файл с другим расширением
        fallback_path = file_path.replace('.md', '.txt')
        if os.path.exists(fallback_path):
            with open(fallback_path, 'r', encoding='utf-8') as f:
                personality_desc = md_to_html(f.read())
        else:
            personality_desc = (
                f"Описание для числа личности {personality_number} пока не готово.\n"
                f"Файл не найден: {file_path}"
            )

    # 🔥 ИСПРАВЛЕНО: Используем \n вместо <br>
    response = (
        f"✨ <b>Ваше число личности: {personality_number}</b>\n\n"
        f"{personality_desc}"
    )

    await message.answer(response, parse_mode="HTML", reply_markup=after_calculation_kb)
    await state.clear()


# 11. ОБРАБОТЧИКИ ДЛЯ ПРОГНОЗА НА ДЕНЬ (остаются без изменений)
@router.callback_query(lambda c: c.data == "daily_forecast")
async def daily_forecast_start(callback: CallbackQuery, state: FSMContext):
    """Начало работы с прогнозом на день"""
    user_id = callback.from_user.id

    if user_id in user_daily_forecast_data:
        try:
            day_number = calculate_day_number(user_daily_forecast_data[user_id])
            text = get_day_text(day_number)
            image_path = get_number_image_path(day_number)

            if os.path.exists(image_path):
                photo = FSInputFile(image_path)
                await callback.message.answer_photo(
                    photo=photo,
                    caption=text,
                    parse_mode="HTML",
                    reply_markup=forecast_menu_kb
                )
            else:
                await callback.message.answer(text, parse_mode="HTML", reply_markup=forecast_menu_kb)
        except Exception as e:
            await callback.message.answer("Произошла ошибка при расчёте. Попробуйте позже.")
    else:
        await callback.message.answer(
            DAILY_FORECAST_INTRO,
            parse_mode="HTML",
            reply_markup=forecast_menu_kb
        )
        await state.set_state(DailyForecastStates.waiting_for_birth_date)
    await callback.answer()


@router.message(DailyForecastStates.waiting_for_birth_date)
async def process_daily_forecast_date(message: Message, state: FSMContext):
    """Обработка введенной даты для прогноза на день"""
    birth_date = message.text.strip()
    user_id = message.from_user.id

    if not validate_date(birth_date):
        await message.answer(
            "❌ Неверный формат даты.\n"
            "Пожалуйста, введи дату как <b>дд.мм.гггг</b>, например:\n"
            "<code>16.02.1995</code>",
            parse_mode="HTML"
        )
        return

    user_daily_forecast_data[user_id] = birth_date

    try:
        day_number = calculate_day_number(birth_date)
        text = get_day_text(day_number)
        image_path = get_number_image_path(day_number)

        if os.path.exists(image_path):
            photo = FSInputFile(image_path)
            await message.answer_photo(
                photo=photo,
                caption=text,
                parse_mode="HTML",
                reply_markup=forecast_menu_kb
            )
        else:
            await message.answer(text, parse_mode="HTML", reply_markup=forecast_menu_kb)
    except Exception as e:
        await message.answer("Произошла ошибка при расчёте. Попробуйте позже.")

    await state.clear()


# 12. ОБРАБОТЧИКИ ДЛЯ СМЕНЫ ДАТЫ (остаются без изменений)
@router.callback_query(F.data == "change_birth_date")
async def change_birth_date(callback: CallbackQuery, state: FSMContext):
    """Смена сохраненной даты рождения"""
    user_id = callback.from_user.id

    if user_id in user_daily_forecast_data:
        del user_daily_forecast_data[user_id]

    await callback.message.answer(
        "Введите новую дату рождения в формате <b>ДД.ММ.ГГГГ</b>, например:\n<code>16.02.1995</code>",
        parse_mode="HTML"
    )
    await state.set_state(DailyForecastStates.waiting_for_birth_date)
    await callback.answer()

# --- КОНЕЦ ФАЙЛА ---