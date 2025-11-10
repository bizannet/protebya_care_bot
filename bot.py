# bot.py - ФИНАЛЬНАЯ ВЕРСИЯ ДЛЯ РОССИИ
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.telegram import TelegramAPIServer  # <-- КЛЮЧЕВОЙ ИМПОРТ
from config.settings import BOT_TOKEN
from handlers.start import router as start_router
from handlers.support_commands import router as support_router
from handlers import numerology, tarot, moon


async def main():
    # 🔥 ИСПОЛЬЗУЕМ ЗЕРКАЛО TELEGRAM API ДЛЯ РОССИИ
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True
        ),
        # ЕДИНСТВЕННАЯ СТРОКА ДЛЯ РАБОТЫ В РФ:
        server=TelegramAPIServer.from_base("https://telega.one")
    )

    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(support_router)
    dp.include_router(numerology.router)
    dp.include_router(tarot.router)
    dp.include_router(moon.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())