import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
YOOKASSA_ACCOUNT_ID = os.getenv("YOOKASSA_ACCOUNT_ID")
YOOKASSA_SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")
# Проверка, что всё загружено
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")