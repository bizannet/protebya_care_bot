# services/tarot_service.py
import random
import os
from aiogram.types import FSInputFile

# Список всех арканов (имена файлов без расширения)
TAROT_CARDS = [
    "fool", "magician", "priestess", "empress", "emperor",
    "hierophant", "lovers", "chariot", "strength", "hermit",
    "wheel_of_fortune", "justice", "hanged_man", "death",
    "temperance", "devil", "tower", "star", "moon", "sun",
    "judgement", "world"
]


def get_random_tarot():
    card_name = random.choice(TAROT_CARDS)

    # Чтение текста
    text_path = os.path.join("texts", "tarot", f"{card_name}.txt")
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    # Загрузка изображения
    photo_path = os.path.join("images", "tarot", f"{card_name}.jpg")
    photo = FSInputFile(photo_path)

    return photo, text