# handlers/__init__.py
from .start import router as start_router
from .support_commands import router as support_commands_router

# Экспортируем под именами, которые используешь в bot.py
start = start_router
support_commands = support_commands_router